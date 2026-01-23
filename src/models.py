from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Mapping, Union
from enum import Enum

# =============================================
# CLI-Internal Enums (for filtering/logic only)
# =============================================

class ReleaseType(str, Enum):
    """CLI-internal: determines which tasks to include"""
    ALBUM = "Album"
    EP = "EP"
    SINGLE = "Single"
    VIDEO = "Video"
    ALL = "All"  # Task applies to all release types

# ============================================================
# GitHub Project Field Enums (actual custom fields in project)
# ============================================================

class Category(str, Enum):
    """GitHub custom field"""
    PRODUCTION = "Production"
    MARKETING = "Marketing"
    RELATIONSHIPS = "Relationships"
    REVENUE = "Revenue"
    CONTENT = "Content"
    INFRASTRUCTURE = "Infrastructure"

class Priority(str, Enum):
    """GitHub custom field"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class Phase(str, Enum):
    """GitHub custom field"""
    PHASE_0 = "Phase 0: Foundation"
    PHASE_1 = "Phase 1: Pre-Production"
    PHASE_2 = "Phase 2: Production"
    PHASE_3 = "Phase 3: Visual Assets"
    PHASE_4 = "Phase 4: Distribution Setup"
    PHASE_5 = "Phase 5: Profile Setup"
    PHASE_6 = "Phase 6: Content Creation"
    PHASE_7 = "Phase 7: Pre-Release Campaign"
    PHASE_8 = "Phase 8: Release Week"
    PHASE_9 = "Phase 9: Post-Release 1-4 Weeks"
    PHASE_10 = "Phase 10: Post-Release 5-8 Weeks"
    ONGOING = "Ongoing Maintenance"

# ==========
# Task Model
# ==========

class Task(BaseModel):
    """
    Task definition combining:
    - CLI-internal metadata (for filtering)
    - GitHub Project field values (to be set on items)
    """
    model_config = ConfigDict(use_enum_values=True)
    
    # ---- CLI-Internal Metadata (not in GitHub) ----
    id: str = Field(..., description="Unique identifier for CLI task tracking")
    release_types: list[ReleaseType] = Field(
        default=[ReleaseType.ALL],
        description="CLI filter: which release types this task applies to"
    )
    depends_on: list[str] = Field(
        default=[],
        description="CLI ordering: list of task IDs this depends on"
    )
    
    # ---- GitHub Project Item Fields ----
    title: str = Field(..., description="GitHub item title")
    body: Optional[str] = Field(None, description="GitHub item description")
    
    # ---- GitHub Project Custom Fields ----
    category: Category = Field(..., description="GitHub custom field: Category")
    priority: Priority = Field(..., description="GitHub custom field: Priority")
    phase: Phase = Field(..., description="GitHub custom field: Phase")
    time_estimate: str = Field(..., description="GitHub custom field: Time Estimate")
    
    def applies_to_release_type(self, release_type: ReleaseType) -> bool:
        """Check if this task should be included for given release type"""
        return ReleaseType.ALL in self.release_types or release_type in self.release_types

# ========================
# CLI Configuration Models
# ========================

class ReleaseConfig(BaseModel):
    """User input configuration for the release"""
    title: str = Field(..., description="Release title (e.g., 'Sojourn Album')")
    release_type: ReleaseType = Field(..., description="CLI filter: Album/EP/Single/Video")
    target_date: str = Field(..., description="Target release date (YYYY-MM-DD)")
    track_count: Optional[int] = Field(None, ge=1, description="Number of tracks (optional)")
    github_owner: str = Field(default="@me", description="GitHub owner login")

class GitHubProjectFields(BaseModel):
    """GitHub Project custom field definitions"""

    category: Mapping[str, Union[str, list[str]]] = Field(
        default={
            "name": "Category",
            "data_type": "SINGLE_SELECT",
            "options": ["Production", "Marketing", "Relationships", "Revenue", "Content", "Infrastructure"]
        }
    )
    priority: Mapping[str, Union[str, list[str]]] = Field(
        default={
            "name": "Priority",
            "data_type": "SINGLE_SELECT",
            "options": ["Critical", "High", "Medium", "Low"]
        }
    )
    phase: Mapping[str, Union[str, list[str]]] = Field(
        default={
            "name": "Phase",
            "data_type": "SINGLE_SELECT",
            "options": [
                "Phase 0: Foundation",
                "Phase 1: Pre-Production",
                "Phase 2: Production",
                "Phase 3: Visual Assets",
                "Phase 4: Distribution Setup",
                "Phase 5: Profile Setup",
                "Phase 6: Content Creation",
                "Phase 7: Pre-Release Campaign",
                "Phase 8: Release Week",
                "Phase 9: Post-Release 1-4 Weeks",
                "Phase 10: Post-Release 5-8 Weeks",
                "Ongoing Maintenance"
            ]
        }
    )
    time_estimate: Mapping[str, Union[str, list[str]]] = Field(
        default={
            "name": "Time Estimate",
            "data_type": "TEXT"
        }
    )

class ProjectMetadata(BaseModel):
    """GitHub Project metadata after creation"""
    id: str = Field(..., description="Project Node ID")
    project_number: int
    project_url: str
    title: str
    owner: str
    field_ids: dict[str, str] = Field(
        default_factory=dict,
        description="Mapping of field names to GitHub field IDs"
    )

class TaskList(BaseModel):
    """Complete task database"""
    version: str = Field(default="1.0", description="Schema version")
    tasks: list[Task]
    
    def filter_by_release_type(self, release_type: ReleaseType) -> list[Task]:
        """Return only tasks applicable to the specified release type"""
        return [
            task for task in self.tasks
            if task.applies_to_release_type(release_type)
        ]
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID"""
        return next((t for t in self.tasks if t.id == task_id), None)