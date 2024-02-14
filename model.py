from sqlmodel import SQLModel, Field, select, create_engine, Session, Relationship
from typing import Optional, List
from sqlalchemy import create_engine


class User(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    name : str
    email : str | None

class Question(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    question_type: str
    options: Optional[List["Options"]] = Relationship(back_populates="question")

class Options(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id", nullable=True)
    option_text: str
    question: Optional[Question] = Relationship(back_populates="options")


class Answers(SQLModel, table = True):
    id : int | None = Field(default = None, primary_key = True)
    selected_option : str 
    question_id : int | None = Field(default = None, foreign_key = "question.id") 
    user_id : int | None = Field(default = None, foreign_key = "user.id")   

#Database URL:     

db_url = "postgresql://aamirlucky60:AhJX4ZpVc8mS@ep-weathered-base-a51yuvs0.us-east-2.aws.neon.tech/Q_app?sslmode=require"
    
engine = create_engine(db_url, echo=True)

#insert data in tables

user_1 = User(name="Aamir", email="abc@mail.com")

question_1 = Question(text="What data type is represented by the following literal?", question_type="single selection")

option_1 = Options(option_text="String",question=question_1)
option_2 = Options(option_text="Integer",question=question_1)
option_3 = Options(option_text="Dictionary",question=question_1)
option_4 = Options(option_text="Boolean",question=question_1)



#add data
#first add user_1, question_1
def add_data():
    with Session(engine) as session:
        session.add(user_1)
        session.add(question_1)
        session.commit()
        session.refresh(user_1)
        session.refresh(question_1)

#second add answer_1
        answer_1 = Answers(selected_option="Boolean", question_id=question_1.id, user_id=user_1.id)
        session.add(answer_1)        
        session.commit()            
def create_tables():
    SQLModel.metadata.create_all(engine)
    

# def delete_heroes():
#     with Session(engine) as session:
#         statement = select(Answers).where(Answers.selected_option == "def function_name(parameters): body")
#         results = session.exec(statement)
#         answer = results.one()
#         session.delete(answer)
#         session.commit()
#         session.refresh(answer)
    
if __name__ == "__main__":
    # create_tables()
    add_data()
    #delete_heroes()
    
    