import { useState } from 'react';

function StudentProfile() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [semester, setSemester] = useState('');

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
            <p>Name: {name}</p>
            <p>Email: {email}</p>
            <p>Semester: {semester}</p>
        </section>
    )
}

export default StudentProfile;