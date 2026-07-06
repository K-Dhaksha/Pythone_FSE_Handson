import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { enroll } from '../store/enrollmentSlice';
import CourseCard from '../components/CourseCard';

function CoursesPage() {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const navigate = useNavigate();
    const dispatch = useDispatch();

    useEffect(() => {
        async function fetchCourses() {
            try {
                const response = await fetch(
                    'https://jsonplaceholder.typicode.com/posts?_limit=5'
                );
                const data = await response.json();
                const mappedCourses = data.map((post, index) => ({
                    id: post.id,
                    name: post.title.slice(0, 30),
                    code: `CS10${index + 1}`,
                    credits: index % 2 === 0 ? 4 : 3,
                    grade: ['A', 'B', 'C', 'A', 'B'][index]
                }));
                setCourses(mappedCourses);
            } catch (err) {
                console.log(err);
            } finally {
                setLoading(false);
            }
        }
        fetchCourses();
    }, []);

    const filteredCourses = courses.filter(course =>
        course.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleEnroll = (course) => {
        dispatch(enroll(course));
        navigate('/profile');
    };

    return (
        <section>
            <h2>Courses</h2>
            <input
                type="text"
                placeholder="Search courses..."
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
            />
            {loading && <p>Loading...</p>}
            <div className="course-grid">
                {filteredCourses.map(course => (
                    <CourseCard
                        key={course.id}
                        {...course}
                        onEnroll={() => handleEnroll(course)}
                    />
                ))}
            </div>
        </section>
    )
}

export default CoursesPage;