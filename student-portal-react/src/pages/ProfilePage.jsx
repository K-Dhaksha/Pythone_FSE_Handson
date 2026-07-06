import { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { unenroll } from '../store/enrollmentSlice';

function ProfilePage() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [semester, setSemester] = useState('');
    const enrolledCourses = useSelector(
        state => state.enrollment.enrolledCourses
    );
    const dispatch = useDispatch();

    return (
        <section>
            <h2>Student Profile</h2>
            <input
                type="text"
                placeholder="Name"
                value={name}
                onChange={e => setName(e.target.value)}
            />
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={e => setEmail(e.target.value)}
            />
            <input
                type="number"
                placeholder="Semester"
                value={semester}
                onChange={e => setSemester(e.target.value)}
            />

            <h3>Enrolled Courses:</h3>
            {enrolledCourses.length === 0 && <p>No courses enrolled yet!</p>}
            {enrolledCourses.map(course => (
                <div key={course.id}>
                    <p>{course.name}</p>
                    <button onClick={() => dispatch(unenroll(course.id))}>
                        Remove
                    </button>
                </div>
            ))}
        </section>
    )
}

export default ProfilePage;