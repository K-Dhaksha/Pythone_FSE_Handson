// ==========================================
// HANDS-ON 7: Alembic Migrations & Versioning
// ==========================================
// All commands are run in the terminal
// Make sure you are in the DatabaseIntegration folder
// ==========================================

// TASK 1: Set Up Alembic and Create Baseline Migration
// ===================================================

// Step 1: Install Alembic
// pip install alembic

// Step 2: Initialize Alembic
// alembic init migrations

// Step 3: Edit alembic.ini
// Find: sqlalchemy.url = driver://user:pass@localhost/dbname
// Replace with: sqlalchemy.url = mysql+mysqlconnector://root:PASSWORD@localhost/college_db_orm

// Step 4: Edit migrations/env.py
// Find: target_metadata = None
// Replace with:
// import sys
// sys.path.append('C:\\Users\\dhaks\\Documents\\PythonFSE\\DatabaseIntegration')
// from models import Base
// target_metadata = Base.metadata

// Step 5: Generate first migration
// alembic revision --autogenerate -m "initial schema"

// Step 6: Apply migration
// alembic upgrade head

// Step 7: Verify
// alembic current
// Expected: shows revision hash
// In SQL client: SHOW TABLES; -- should show alembic_version table


// TASK 2: Add and Apply Incremental Migrations
// ============================================

// Step 8: Add is_active column to Student model in models.py
// is_active = Column(Boolean, default=True)

// Step 9: Generate migration
// alembic revision --autogenerate -m "add is_active to students"

// Step 10: Inspect generated file in migrations/versions/
// Should contain:
// def upgrade():
//     op.add_column('students', sa.Column('is_active', sa.Boolean(), nullable=True))
// def downgrade():
//     op.drop_column('students', 'is_active')

// Step 11: Apply migration
// alembic upgrade head

// Step 12: Verify in SQL client
// DESCRIBE students; -- should show is_active column

// Step 13: Add CourseSchedule model to models.py
// class CourseSchedule(Base):
//     __tablename__ = 'course_schedules'
//     schedule_id = Column(Integer, primary_key=True, autoincrement=True)
//     course_id = Column(Integer, ForeignKey('courses.course_id'))
//     day_of_week = Column(String(20))
//     start_time = Column(Time)
//     end_time = Column(Time)

// Step 14: Generate migration
// alembic revision --autogenerate -m "add course schedules table"

// Step 15: Apply migration
// alembic upgrade head

// Step 16: Check migration history
// alembic history --verbose
// Expected: 3 revisions listed

// Step 17: Verify in SQL client
// SHOW TABLES; -- should show course_schedules
// DESCRIBE course_schedules;


// TASK 3: Rollback and Recovery
// ==============================

// Step 18: Note current revision
// alembic current
// Copy the hash shown e.g. a1b2c3d4e5f6

// Step 19: Rollback one step
// alembic downgrade -1
// Verify in SQL client:
// DESCRIBE students; -- is_active column should be gone

// Step 20: Rollback ALL the way
// alembic downgrade base
// Verify in SQL client:
// SHOW TABLES; -- all tables should be gone except alembic_version

// Step 21: Re-apply everything
// alembic upgrade head
// Verify in SQL client:
// SHOW TABLES;
// DESCRIBE students;       -- is_active should be back
// DESCRIBE course_schedules; -- should exist

// Step 22: Confirm current matches head
// alembic current
// Should match the latest revision hash 


// ROLLBACK ANALYSIS
// =================
// alembic downgrade -1   → removes is_active column only
// alembic downgrade base → removes ALL migration changes
// alembic upgrade head   → reapplies ALL migrations
