from datetime import datetime
from sqlalchemy import String,Float,Integer,Text,DateTime,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from .db import Base
class Project(Base):
 __tablename__='projects'; id:Mapped[int]=mapped_column(Integer,primary_key=True); name:Mapped[str]=mapped_column(String(200)); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); evidence=relationship('Evidence',back_populates='project',cascade='all, delete-orphan'); time_entries=relationship('TimeEntry',back_populates='project',cascade='all, delete-orphan')
class Evidence(Base):
 __tablename__='evidence'; id:Mapped[int]=mapped_column(Integer,primary_key=True); project_id:Mapped[int]=mapped_column(ForeignKey('projects.id')); source:Mapped[str]=mapped_column(String(50)); external_id:Mapped[str]=mapped_column(String(300)); issue_key:Mapped[str|None]=mapped_column(String(100),nullable=True); event_type:Mapped[str]=mapped_column(String(100)); actor:Mapped[str|None]=mapped_column(String(200),nullable=True); timestamp:Mapped[datetime|None]=mapped_column(DateTime,nullable=True); text:Mapped[str|None]=mapped_column(Text,nullable=True); metadata_json:Mapped[str]=mapped_column(Text,default='{}'); ai_signal:Mapped[float]=mapped_column(Float,default=0); evidence_strength:Mapped[float]=mapped_column(Float,default=0); project=relationship('Project',back_populates='evidence')
class TimeEntry(Base):
 __tablename__='time_entries'; id:Mapped[int]=mapped_column(Integer,primary_key=True); project_id:Mapped[int]=mapped_column(ForeignKey('projects.id')); date:Mapped[str]=mapped_column(String(20)); user:Mapped[str]=mapped_column(String(200)); issue_key:Mapped[str]=mapped_column(String(100)); hours:Mapped[float]=mapped_column(Float); hourly_cost:Mapped[float]=mapped_column(Float); project=relationship('Project',back_populates='time_entries')
