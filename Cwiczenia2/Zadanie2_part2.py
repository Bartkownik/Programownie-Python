import random
from datetime import datetime
from sqlalchemy import create_engine, select, update, delete, func
from sqlalchemy.orm import Session
from models_zadaniepart2 import Experiment, DataPoint

engine = create_engine("sqlite:///test.db", echo=True)


def main():
  
    with Session(engine) as session:
        exp1 = Experiment(title="Eksperyment 1", created_at=datetime.now(), type=1)
        exp2 = Experiment(title="Eksperyment 2", created_at=datetime.now(), type=2)

        for exp in (exp1, exp2):
            for _ in range(10):
                exp.data_points.append(DataPoint(
                    real_value=round(random.uniform(0, 100), 2),
                    target_value=round(random.uniform(0, 100), 2),
                ))

        session.add_all([exp1, exp2])
        session.commit()


    with Session(engine) as session:
        for exp in session.scalars(select(Experiment)):
            print(" ", exp)
        for dp in session.scalars(select(DataPoint)):
            print(" ", dp)


    with Session(engine) as session:
        session.execute(update(Experiment).values(finished=True))
        session.commit()
        for exp in session.scalars(select(Experiment)):
            print(" ", exp)


    stmt = (
        select(
            Experiment.title,
            func.sum(DataPoint.real_value),
            func.avg(DataPoint.real_value),
        )
        .join(Experiment.data_points)
        .group_by(Experiment.id, Experiment.title)
    )
    with Session(engine) as session:
        for title, suma, srednia in session.execute(stmt):
            print(f"{title}: suma={suma:.2f}, średnia={srednia:.2f}")


    with Session(engine) as session:
        session.execute(delete(DataPoint))
        session.execute(delete(Experiment))
        session.commit()


if __name__ == "__main__":
    main()