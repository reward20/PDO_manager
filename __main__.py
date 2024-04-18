from collections import defaultdict
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Query
from File_find import Getter_files
from Ml_ex import MLEXCEL_reader, MLEXCELO_parcer
import pandas as pd
from src import ML_O_correct, db_engine

from src import (
    settings,
    db_session,
    db_engine,
    Mlexcel_model,
    ML_O_Model,
    Base,
)

# t = Getter_files(path_dir=r"Data\dos_file", suffix="")
# for x in t.search_files():
#     if x.stem == "MLEXCEL":
#         obj = MLEXCEL_reader(MLEXCEL_path=x)
#         obj.read_file()
#     print(x.stem)

if __name__ == "__main__":
    t = Getter_files(
        path_dir=settings.DOS_FOLDER,
        suffix=settings.FILES_SUFFIX_DOS
        )
    print(settings.MLE_engine)
    # Mlexcel_model.__table__.drop(db_engine)
    # Mlexcel_model.__table__.create(db_engine)
    Base.metadata.drop_all(db_engine)
    Base.metadata.create_all(db_engine)

    for x in t.search_files():
        if x.stem == "MLEXCELO":
            objs = MLEXCELO_parcer(MLEXCELO_path=x)
            with db_engine.connect() as connect:


            # with db_session() as session:
                check_set = set()
                # session.begin()
                time_m = datetime.now()

                for obj in objs.read_file():
                    if (obj.detail_num, obj.operation_num) in check_set:
                        continue

                    check_set.add((obj.detail_num, obj.operation_num))
                    # model = ML_O_Model(**obj.model_dump())
                    connect.execute(
                        ML_O_Model.__table__.insert(), obj.model_dump()
                    )
                connect.commit()
                # session.add(model)
                # table = pd.DataFrame(my_dict)
                # table.index.name = 'id'
                # table.to_sql(ML_O_Model.__tablename__, session.connection(), if_exists="replace", schema=ML_O_correct)
                # session.commit()
                print(f"{datetime.now() - time_m}")
                with db_session() as session:
                    stmt = select(ML_O_Model).where(ML_O_Model.detail_num == "УФГ3000-1.041/402")
                    for x in session.execute(stmt).scalars():
                        print(x.detail_num)








        # if x.stem == "MLEXCEL":
        #     obj = MLEXCEL_reader(MLEXCEL_path=x)
        #     with db_session() as session:
        #         session.delete
        #         session.begin()
        #         try:
        #             for x in obj.read_file():
        #                 model = Mlexcel_model(**x.model_dump())
        #                 session.add(model)
        #         except Exception as e:
        #             session.rollback()
        #             raise e
        #         else:
        #             session.commit()
