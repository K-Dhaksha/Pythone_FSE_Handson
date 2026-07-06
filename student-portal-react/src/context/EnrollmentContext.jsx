import { createContext, useContext, useState } from 'react';

const EnrollmentContext = createContext();

export function EnrollmentProvider({ children }) {
    const [enrolledCourses, setEnrolledCourses] = useState([]);

    const enroll = (course) => {
        if (!enrolledCourses.find(c => c.id === course.id)) {
            setEnrolledCourses([...enrolledCourses, course]);
        }
    };

    const unenroll = (courseId) => {
        setEnrolledCourses(enrolledCourses.filter(c => c.id !== courseId));
    };

    return (
        <EnrollmentContext.Provider value={{ enrolledCourses, enroll, unenroll }}>
            {children}
        </EnrollmentContext.Provider>
    );
}

export function useEnrollment() {
    return useContext(EnrollmentContext);
}