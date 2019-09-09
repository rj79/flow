from flask_sqlalchemy import SQLAlchemy

"""
Instantiating the database here to avoid circular import dependencies
"""
db = SQLAlchemy()
