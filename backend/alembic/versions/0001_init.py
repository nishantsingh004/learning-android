"""initial migration"""

revision = "0001_init"      # or a UUID-like id – must be unique
down_revision = None        # since this is your first migration
branch_labels = None
depends_on = None


from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('phone', sa.String(length=20), unique=True),
        sa.Column('role', sa.String(length=20), nullable=False, server_default='farmer'),
        sa.Column('locale', sa.String(length=10), server_default='hi-IN'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'))
    )
    op.create_table('farmers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('name', sa.Text()),
        sa.Column('village', sa.Text()),
        sa.Column('district', sa.Text()),
        sa.Column('state', sa.Text()),
        sa.Column('lat', sa.Numeric()),
        sa.Column('lon', sa.Numeric()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'))
    )
    op.create_table('fields',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('farmer_id', sa.Integer(), sa.ForeignKey('farmers.id', ondelete='CASCADE')),
        sa.Column('area_acres', sa.Numeric(8,2)),
        sa.Column('soil_type', sa.Text()),
        sa.Column('irrigation', sa.Text()),
        sa.Column('geom', Geography(geometry_type='POLYGON', srid=4326))
    )
    op.create_table('crops',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name_en', sa.Text()),
        sa.Column('name_hi', sa.Text()),
        sa.Column('category', sa.Text())
    )
    op.create_table('crop_prices',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('crop_id', sa.Integer(), sa.ForeignKey('crops.id')),
        sa.Column('mandi', sa.Text()),
        sa.Column('price_per_quintal', sa.Numeric(10,2)),
        sa.Column('price_date', sa.Date())
    )
    op.create_table('recommendations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('field_id', sa.Integer(), sa.ForeignKey('fields.id', ondelete='CASCADE')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('top1_crop_id', sa.Integer(), sa.ForeignKey('crops.id')),
        sa.Column('top1_profit', sa.Numeric(12,2)),
        sa.Column('top1_demand_score', sa.Integer()),
        sa.Column('top1_risk_score', sa.Integer()),
        sa.Column('top2_crop_id', sa.Integer(), sa.ForeignKey('crops.id')),
        sa.Column('top2_profit', sa.Numeric(12,2)),
        sa.Column('top2_demand_score', sa.Integer()),
        sa.Column('top2_risk_score', sa.Integer()),
        sa.Column('top3_crop_id', sa.Integer(), sa.ForeignKey('crops.id')),
        sa.Column('top3_profit', sa.Numeric(12,2)),
        sa.Column('top3_demand_score', sa.Integer()),
        sa.Column('top3_risk_score', sa.Integer()),
        sa.Column('details', sa.JSON())
    )
    op.create_table('advisories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('farmer_id', sa.Integer(), sa.ForeignKey('farmers.id', ondelete='CASCADE')),
        sa.Column('field_id', sa.Integer(), sa.ForeignKey('fields.id', ondelete='CASCADE')),
        sa.Column('crop_id', sa.Integer(), sa.ForeignKey('crops.id')),
        sa.Column('text', sa.Text()),
        sa.Column('audio_url', sa.Text()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'))
    )
    op.create_table('feedback',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('farmer_id', sa.Integer(), sa.ForeignKey('farmers.id')),
        sa.Column('advisory_id', sa.Integer(), sa.ForeignKey('advisories.id')),
        sa.Column('rating', sa.Integer()),
        sa.Column('comment', sa.Text()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'))
    )

def downgrade():
    op.drop_table('feedback')
    op.drop_table('advisories')
    op.drop_table('recommendations')
    op.drop_table('crop_prices')
    op.drop_table('crops')
    op.drop_table('fields')
    op.drop_table('farmers')
    op.drop_table('users')
