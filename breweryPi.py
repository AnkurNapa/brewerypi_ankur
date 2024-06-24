import click
from flask import current_app
from flask_migrate import Migrate, upgrade
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash
from app import createApp, db
from app.models import (
    Area, Element, ElementAttribute, ElementAttributeTemplate, 
    ElementTemplate, Enterprise, EventFrame, EventFrameAttribute, 
    EventFrameAttributeTemplate, EventFrameAttributeTemplateEventFrameTemplateView, 
    EventFrameEventFrameGroup, EventFrameGroup, EventFrameNote, 
    EventFrameTemplate, EventFrameTemplateView, Lookup, LookupValue, 
    Message, Permission, Note, Role, Site, Tag, TagValue, TagValueNote, 
    UnitOfMeasurement, User
)

application = app = createApp()
migrate = Migrate(app, db, directory="db/migrations")

@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app, db=db, Area=Area, Element=Element, ElementAttribute=ElementAttribute, 
        ElementAttributeTemplate=ElementAttributeTemplate, ElementTemplate=ElementTemplate, 
        Enterprise=Enterprise, EventFrame=EventFrame, EventFrameAttribute=EventFrameAttribute, 
        EventFrameAttributeTemplate=EventFrameAttributeTemplate, 
        EventFrameAttributeTemplateEventFrameTemplateView=EventFrameAttributeTemplateEventFrameTemplateView, 
        EventFrameEventFrameGroup=EventFrameEventFrameGroup, EventFrameGroup=EventFrameGroup, 
        EventFrameNote=EventFrameNote, EventFrameTemplate=EventFrameTemplate, 
        EventFrameTemplateView=EventFrameTemplateView, Lookup=Lookup, 
        LookupValue=LookupValue, Message=Message, Note=Note, Role=Role, 
        Site=Site, Tag=Tag, TagValue=TagValue, TagValueNote=TagValueNote, 
        UnitOfMeasurement=UnitOfMeasurement, User=User
    )

@app.cli.command("deploy")
@click.option("--admin", is_flag=True, help='Add the default admin ("pi") user. Requires default roles.')
@click.option("--roles", is_flag=True, help="Add the default roles.")
def deploy(admin, roles):
    print(f"Creating database {current_app.config['MYSQL_DATABASE']} if it does not exist...")
    engine = create_engine(current_app.config["SQLALCHEMY_SERVER_URI"])
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {current_app.config['MYSQL_DATABASE']}"))
        print("Running database upgrade...")
        upgrade()
        if roles or admin:
            engine = create_engine(current_app.config["SQLALCHEMY_DATABASE_URI"])
            connection = engine.connect()
            if roles:
                print("Inserting default roles if needed...")
                connection.execute(text(f"INSERT INTO `Role` (`Name`, `Permissions`) VALUES ('User', {Permission.DATA_ENTRY})"))
                connection.execute(text(f"INSERT INTO `Role` (`Name`, `Permissions`) VALUES ('Administrator', 0xff)"))

            if admin:
                print("Inserting default administrator if needed...")
                administratorRoleId = connection.execute(text("SELECT RoleId FROM Role WHERE Name = 'Administrator'")).scalar()
                if administratorRoleId is None:
                    print('Administrator role does not exist. Cannot create default admin/"pi" user without it.')
                else:
                    password = generate_password_hash("brewery", method="pbkdf2")
                    connection.execute(text(f"INSERT INTO `User` (`Enabled`, `Name`, `PasswordHash`, `RoleId`) VALUES (1, 'pi', '{password}', {administratorRoleId})"))

        connection.commit()

if __name__ == "__main__":
    app.run()
