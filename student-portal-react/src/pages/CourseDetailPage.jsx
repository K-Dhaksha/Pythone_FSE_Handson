import { useParams, useNavigate } from 'react-router-dom';

function CourseDetailPage() {
    const { courseId } = useParams();
    const navigate = useNavigate();

    return (
        <section>
            <h2>Course Detail</h2>
            <p>Course ID: {courseId}</p>
            <button onClick={() => navigate('/profile')}>
                Enroll
            </button>
            <button onClick={() => navigate('/courses')}>
                Back to Courses
            </button>
        </section>
    )
}

export default CourseDetailPage;