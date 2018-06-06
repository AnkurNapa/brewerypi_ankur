"""empty message

Revision ID: c4482c3bf78e
Revises: f64c7735ec58
Create Date: 2018-06-01 19:44:43.926861

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = 'c4482c3bf78e'
down_revision = 'f64c7735ec58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ElementAttributeTemplate',
    sa.Column('ElementAttributeTemplateId', sa.Integer(), nullable=False),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('ElementTemplateId', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.ForeignKeyConstraint(['ElementTemplateId'], ['ElementTemplate.ElementTemplateId'], name='FK__ElementTemplate$Have$ElementAttributeTemplate'),
    sa.PrimaryKeyConstraint('ElementAttributeTemplateId'),
    sa.UniqueConstraint('ElementTemplateId', 'Name', name='AK__ElementTemplateId__Name')
    )

    # Insert AttributeTemplate records to ElementAttributeTemplate.
    metadata = sa.MetaData()
    metadata.reflect(bind = op.get_bind())
    attributeTemplates = metadata.tables["AttributeTemplate"]
    elementAttributeTemplates = metadata.tables["ElementAttributeTemplate"]
    selectStatement = sa.select([attributeTemplates])
    resultProxy = op.get_bind().execute(selectStatement)
    for record in resultProxy:
        insertStatement = elementAttributeTemplates.insert().values(ElementAttributeTemplateId = record.AttributeTemplateId, Description = record.Description,
            ElementTemplateId = record.ElementTemplateId, Name = record.Name)
        op.get_bind().execute(insertStatement)

    op.create_table('EventFrameAttributeTemplate',
    sa.Column('EventFrameAttributeTemplateId', sa.Integer(), nullable=False),
    sa.Column('Description', sa.String(length=255), nullable=True),
    sa.Column('EventFrameTemplateId', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.ForeignKeyConstraint(['EventFrameTemplateId'], ['EventFrameTemplate.EventFrameTemplateId'], name='FK__EventFrameTemplate$Have$EventFrameAttributeTemplate'),
    sa.PrimaryKeyConstraint('EventFrameAttributeTemplateId'),
    sa.UniqueConstraint('EventFrameTemplateId', 'Name', name='AK__EventFrameTemplateId__Name')
    )
    op.create_table('EventFrameAttribute',
    sa.Column('EventFrameAttributeId', sa.Integer(), nullable=False),
    sa.Column('EventFrameAttributeTemplateId', sa.Integer(), nullable=False),
    sa.Column('EventFrameId', sa.Integer(), nullable=False),
    sa.Column('TagId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['EventFrameAttributeTemplateId'], ['EventFrameAttributeTemplate.EventFrameAttributeTemplateId'], name='FK__EventFrameAttributeTemplate$Have$EventFrameAttribute'),
    sa.ForeignKeyConstraint(['EventFrameId'], ['EventFrame.EventFrameId'], name='FK__EventFrame$Have$EventFrameAttribute'),
    sa.ForeignKeyConstraint(['TagId'], ['Tag.TagId'], name='FK__Tag$Have$EventFrameAttribute'),
    sa.PrimaryKeyConstraint('EventFrameAttributeId'),
    sa.UniqueConstraint('EventFrameAttributeTemplateId', 'EventFrameId', name='AK__EventFrameAttributeTemplateId__EventFrameId')
    )
    op.drop_constraint('FK__ElementTemplate$Have$AttributeTemplate', 'AttributeTemplate', type_='foreignkey') # Here
    op.drop_index('AK__ElementTemplateId__Name', table_name='AttributeTemplate')
    op.drop_constraint('FK__AttributeTemplate$Have$ElementAttribute', 'ElementAttribute', type_='foreignkey') # Here
    op.drop_table('AttributeTemplate')
    op.add_column('ElementAttribute', sa.Column('ElementAttributeTemplateId', sa.Integer(), nullable=False))

    # Update ElementAttributeTemplateId to AttributeTemplateId.
    metadata2 = sa.MetaData()
    metadata2.reflect(bind = op.get_bind())
    elementAttributes = metadata2.tables["ElementAttribute"]
    updateStatement = elementAttributes.update().values(ElementAttributeTemplateId = elementAttributes.c.AttributeTemplateId)
    op.get_bind().execute(updateStatement)

    op.create_unique_constraint('AK__ElementAttributeTemplateId__ElementId', 'ElementAttribute', ['ElementAttributeTemplateId', 'ElementId'])
    op.drop_index('AK__AttributeTemplateId__ElementId', table_name='ElementAttribute')
    #op.drop_constraint('FK__AttributeTemplate$Have$ElementAttribute', 'ElementAttribute', type_='foreignkey') Here
    op.create_foreign_key('FK__ElementAttributeTemplate$Have$ElementAttribute', 'ElementAttribute', 'ElementAttributeTemplate', ['ElementAttributeTemplateId'], ['ElementAttributeTemplateId'])
    op.drop_column('ElementAttribute', 'AttributeTemplateId')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ElementAttribute', sa.Column('AttributeTemplateId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_constraint('FK__ElementAttributeTemplate$Have$ElementAttribute', 'ElementAttribute', type_='foreignkey')
    #op.create_foreign_key('FK__AttributeTemplate$Have$ElementAttribute', 'ElementAttribute', 'AttributeTemplate', ['AttributeTemplateId'], ['AttributeTemplateId']) Here

    # Update AttributeTemplateId to ElementAttributeTemplateId.
    metadata = sa.MetaData()
    metadata.reflect(bind = op.get_bind())
    elementAttributes = metadata.tables["ElementAttribute"]
    updateStatement = elementAttributes.update().values(AttributeTemplateId = elementAttributes.c.ElementAttributeTemplateId)
    op.get_bind().execute(updateStatement)

    op.create_index('AK__AttributeTemplateId__ElementId', 'ElementAttribute', ['AttributeTemplateId', 'ElementId'], unique=True)
    op.drop_constraint('AK__ElementAttributeTemplateId__ElementId', 'ElementAttribute', type_='unique')
    op.drop_column('ElementAttribute', 'ElementAttributeTemplateId')
    op.create_table('AttributeTemplate',
    sa.Column('AttributeTemplateId', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('Description', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('ElementTemplateId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('Name', mysql.VARCHAR(length=45), nullable=False),
    sa.ForeignKeyConstraint(['ElementTemplateId'], ['ElementTemplate.ElementTemplateId'], name='FK__ElementTemplate$Have$AttributeTemplate'),
    sa.PrimaryKeyConstraint('AttributeTemplateId'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )

    # Insert ElementAttributeTemplate records to AttributeTemplate.
    metadata2 = sa.MetaData()
    metadata2.reflect(bind = op.get_bind())
    attributeTemplates = metadata2.tables["AttributeTemplate"]
    elementAttributeTemplates = metadata2.tables["ElementAttributeTemplate"]
    selectStatement = sa.select([elementAttributeTemplates])
    resultProxy = op.get_bind().execute(selectStatement)
    for record in resultProxy:
        insertStatement = attributeTemplates.insert().values(AttributeTemplateId = record.ElementAttributeTemplateId, Description = record.Description,
            ElementTemplateId = record.ElementTemplateId, Name = record.Name)
        op.get_bind().execute(insertStatement)

    op.create_foreign_key('FK__AttributeTemplate$Have$ElementAttribute', 'ElementAttribute', 'AttributeTemplate', ['AttributeTemplateId'], ['AttributeTemplateId']) # Here
    op.create_index('AK__ElementTemplateId__Name', 'AttributeTemplate', ['ElementTemplateId', 'Name'], unique=True)
    op.drop_table('EventFrameAttribute')
    op.drop_table('EventFrameAttributeTemplate')
    op.drop_table('ElementAttributeTemplate')
    # ### end Alembic commands ###
