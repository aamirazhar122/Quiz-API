from model import User, Question, Options, Answers, engine, Session, SQLModel, select
from typing import List, Annotated, Optional
from fastapi import FastAPI, HTTPException, status, Depends

class CreateUser(SQLModel):
    name : str
    email : str | None = None

class UserResponse(SQLModel):
    id : int
    name: str
    email : str

class UpdateUser(SQLModel):
    name : Optional[str] = None
    email : Optional[str] = None    

class QuestionResponse(SQLModel):
    id : int
    text : str
    question_type : str

class CreateQuestion(SQLModel):
    text : str | None = None
    question_type : str | None = None

class CreateOptions(SQLModel):
    
    option_text : str | None = None
    question_id : int | None = None

class ResponseOptions(SQLModel):
    id : int 
    option_text : str
    question_id : int             

class CreateAnswers(SQLModel):
    selected_option : str | None = None
    question_id : int | None = None
    user_id : int | None = None

class ResponseAnswers(SQLModel):
    id : int 
    selected_option : str
    question_id : int
    user_id : int             

app : FastAPI = FastAPI()


#Dependancy injection
def get_db():
    with Session(engine) as session:
        yield session


#get method for User(gt all users list) 
@app.get("/user", response_model=List[User])
def get_user(session: Annotated[Session,Depends(get_db)]):
    user = session.exec(select(User)).all()
    return user

#get method for Users(get users by id)
@app.get("/user/{id}", response_model=UserResponse)
def get_user_by_id(id : int,session : Annotated[Session, Depends(get_db)]):
    user = session.get(User, id)
    if not user : 
        raise HTTPException(status_code=404, detail="user not found")
    return user

#post method for users
@app.post("/users",response_model=UserResponse)
def post_user(user : CreateUser, session:Annotated[Session, Depends(get_db)]):
    users_to_insert = User.model_validate(user)
    session.add(users_to_insert)
    session.commit()
    session.refresh(users_to_insert)
    return users_to_insert

#Update method for Users
@app.patch("/user/{id}", response_model=UserResponse)
def patch_user(id : int, user_data : UpdateUser ,session : Annotated[Session, Depends(get_db)]):
    user = session.get(User, id)
    if not user : 
        raise HTTPException(status_code=404, detail="user not found")
    user_to_dict = user_data.model_dump(exclude_unset=True)
    
    for key, value in user_to_dict.items():
        setattr(user, key, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

#Delete method for Users
@app.delete("/user/{id}")
def delete_user(id : int, session:Annotated[Session, Depends(get_db)]):
    user = session.get(User, id)
    if not user : 
        raise HTTPException(status_code=404, detail="user not found")
    
    answer_to_delete = session.exec(select(Answers).where(Answers.user_id == id)).all()
    for answer in answer_to_delete :
        session.delete(answer)
    
    session.delete(user)
    session.commit()
    return {"message" : "user delete successfully"}

#get method for Question(get all questions)
@app.get("/question", response_model=List[Question])
def get_question(session : Annotated[Session,Depends(get_db)]):
    questions = session.exec(select(Question)).all()
    return questions

#get method for Question(get Questions by id)
@app.get("/question/{id}", response_model=QuestionResponse)
def get_question_by_id (q_id : int, session:Annotated[Session, Depends(get_db)]):
    questions = session.get(Question, q_id)
    if not questions:
        raise HTTPException(status_code=404, detail="question not found")
    return questions

#post method for Questions
@app.post("/question",response_model=QuestionResponse)
def post_question(question : CreateQuestion, session : Annotated[Session, Depends(get_db)]):
    question_to_insert = Question.model_validate(question)
    session.add(question_to_insert)
    session.commit()
    session.refresh(question_to_insert)
    return question_to_insert

#update method for Questions
@app.patch("/question/{id}", response_model=QuestionResponse)
def patch_question(id : int, question_data : CreateQuestion, session : Annotated[Session, Depends(get_db)]):
    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    question_to_dict = question_data.model_dump(exclude_unset=True)

    for key, value in question_to_dict.items():
        setattr(question, key, value)

    session.add(question)
    session.commit()
    session.refresh(question)
    return question

#Delete method for Question
@app.delete("/question/{id}")
def delete_question(id : int, session : Annotated[Session, Depends(get_db)]):
    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="question not found")
    
    answer_to_delete = session.exec(select(Answers).where(Answers.question_id == id)).all()
    for answer in answer_to_delete :
        session.delete(answer)
    
    option_to_delete = session.exec(select(Options).where(Options.question_id == id)).all()
    for option in option_to_delete :
        session.delete(option)
    
    session.delete(question)
    session.commit()
    return {"message" : "Question successfully deleted"}



#get method for Options(get all options)
@app.get("/options", response_model=List[Options])
def get_options(session : Annotated[Session, Depends(get_db)]):
    options = session.exec(select(Options)).all()
    return options

#get method for Options(get options by id)
@app.get("/options/{id}")
def get_options_by_id(id : int, session : Annotated[Session, Depends(get_db)]):
    options = session.get(Options, id)
    if not options:
        raise HTTPException(status_code=404, detail="options not found")
    return options

#post method for options
@app.post("/options", response_model=ResponseOptions)
def post_option(option : CreateOptions, session : Annotated[Session, Depends(get_db)]):
    options_to_insert = Options.model_validate(option)    
    session.add(options_to_insert)
    session.commit()
    session.refresh(options_to_insert)
    return options_to_insert

#update method for options
@app.patch("/options/{id}", response_model=ResponseOptions)
def patch_options(id : int, option_data : CreateOptions, session : Annotated[Session, Depends(get_db)]):
    option = session.get(Options, id)   
    if not option:
        raise HTTPException(status_code=404, detail= " option not found")
    option_to_dict = option_data.model_dump(exclude_unset=True)

    for key, value in option_to_dict.items():
        setattr(option, key, value)

    session.add(option)
    session.commit()
    session.refresh(option)
    return option    

#Delete method for Options
@app.delete("/options/{id}")
def delete_option(id : int, session : Annotated[Session, Depends(get_db)]):
    option = session.get(Options, id)
    if not option:
        raise HTTPException(status_code=404, detail="option not found")   
    session.delete(option)
    session.commit()
    return {"message" : "option deleted successfully"}

#get method for Answers(get all answers)
@app.get("/answers", response_model=List[Answers])
def get_answer(session : Annotated[Session, Depends(get_db)]):
    answer = session.exec(select(Answers)).all()
    return answer

#get method for Answers(get answers by id)
@app.get("/answers/{id}")
def get_answers_by_id(id : int, session : Annotated[Session, Depends(get_db)]):
    answer = session.get(Answers, id)
    if not answer :
        raise HTTPException(status_code=404,detail="answer not found")
    return answer

#post method of answer
@app.post("/answers", response_model=ResponseAnswers)
def post_answer(answer : CreateAnswers, session : Annotated[Session, Depends(get_db)]):
    answers_to_insert = Answers.model_validate(answer)
    session.add(answers_to_insert)
    session.commit()
    session.refresh(answers_to_insert)
    return answers_to_insert

#update method for answers
@app.patch("/answers/{id}", response_model=ResponseAnswers)
def patch_answer(id : int, answer_data : CreateAnswers, session : Annotated[Session, Depends(get_db)]):
    answer = session.get(Answers, id)
    if not answer:
        raise HTTPException(status_code=404, detail="answer not found")
    answer_to_dict = answer_data.model_dump(exclude_unset=True)
    
    for key, value in answer_to_dict.items():
        setattr(answer, key, value)

    session.add(answer)
    session.commit()
    session.refresh(answer)
    return answer

#Delete method for Answers
@app.delete("/answers/{id}")
def delete_answer(id : int, session : Annotated[Session, Depends(get_db)]):
    answer = session.get(Answers, id)
    if not answer :
        raise HTTPException(status_code=404, detail="answer not found")
    
    session.delete(answer)
    session.commit()
    return {"message" : "Answer deleted successfully"}
