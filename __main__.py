from File_find import Getter_files
from Ml_ex import MLEXCEL_reader

from src.config import settings
from src import db_session, db_engine
from schemas import Mlexcel_model, Base


# t = Getter_files(path_dir=r"Data\dos_file", suffix="")
# for x in t.search_files():
#     if x.stem == "MLEXCEL":
#         obj = MLEXCEL_reader(MLEXCEL_path=x)
#         obj.read_file()
#     print(x.stem)

if __name__ == "__main__":
    t = Getter_files(path_dir=settings.DOS_FOLDER, suffix=settings.FILES_SUFFIX_DOS)
    print(settings.MLE_engine)
    Base.metadata.create_all(db_engine)
    for x in t.search_files():
        if x.stem == "MLEXCEL":
            obj = MLEXCEL_reader(MLEXCEL_path=x)
            with db_session() as session:
                session.begin()
                try:
                    for x in obj.read_file():
                        model = Mlexcel_model(**x.model_dump())
                        
                        print(session.add(model))
                        break
                except:
                    session.rollback()
                    raise
                else:
                    session.commit()
