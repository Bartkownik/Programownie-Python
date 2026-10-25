from datetime import datetime
from sqlalchemy import String, ForeignKey, Column, Table, false
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


experiment_subject = Table(
    "experiment_subject",
    Base.metadata,
    Column("experiment_id", ForeignKey("Experiment.id"), primary_key=True),
    Column("subject_id", ForeignKey("Subject.id"), primary_key=True),
)


class Experiment(Base):
    __tablename__ = "Experiment"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime]
    type: Mapped[int]
    finished: Mapped[bool] = mapped_column(default=False)

    data_points: Mapped[list["DataPoint"]] = relationship(back_populates="experiment")
    subjects: Mapped[list["Subject"]] = relationship(
        secondary=experiment_subject, back_populates="experiments"
    )

    def __repr__(self):
        return f"Experiment(id={self.id}, title={self.title!r}, type={self.type}, finished={self.finished})"


class DataPoint(Base):
    __tablename__ = "DataPoint"

    id: Mapped[int] = mapped_column(primary_key=True)
    real_value: Mapped[float]
    target_value: Mapped[float]

    experiment_id: Mapped[int] = mapped_column(ForeignKey("Experiment.id"))
    experiment: Mapped["Experiment"] = relationship(back_populates="data_points")

    def __repr__(self):
        return f"DataPoint(id={self.id}, real={self.real_value}, target={self.target_value})"


class Subject(Base):
    __tablename__ = "Subject"

    id: Mapped[int] = mapped_column(primary_key=True)
    gdpr_accepted: Mapped[bool] = mapped_column(default=False, server_default=false())

    experiments: Mapped[list["Experiment"]] = relationship(
        secondary=experiment_subject, back_populates="subjects"
    )

    def __repr__(self):
        return f"Subject(id={self.id}, gdpr_accepted={self.gdpr_accepted})"