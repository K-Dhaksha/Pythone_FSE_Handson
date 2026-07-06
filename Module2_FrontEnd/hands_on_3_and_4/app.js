import { courses } from "./data.js";

courses.forEach(course => {
    const { name, credits } = course;
    console.log(name, credits);
});

const formatted = courses.map(
    course => `${course.code} — ${course.name} (${course.credits} credits)`
);
console.log(formatted);

const highCredit = courses.filter(course => course.credits >= 4);
console.log(highCredit.length);

const totalCredits = courses.reduce(
    (total, course) => total + course.credits, 0
);
console.log(totalCredits);

const grid = document.querySelector(".course-grid");
const totalPara = document.querySelector("#total-credits");
const searchInput = document.querySelector("#search-courses");
const sortButton = document.querySelector("#sort-btn");
const selectedCourse = document.querySelector("#selected-course");

function renderCourses(courseArray) {
    grid.innerHTML = "";

    courseArray.forEach(course => {
        const article = document.createElement("article");
        article.className = "course-card";
        article.dataset.id = course.id;
        article.innerHTML = `
            <h3>${course.name}</h3>
            <p>${course.code}</p>
            <span>${course.credits} Credits</span>
        `;
        grid.appendChild(article);
    });

    const credits = courseArray.reduce(
        (total, course) => total + course.credits, 0
    );
    totalPara.textContent = `Total Credits: ${credits}`;
}

function fetchAllCourses() {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(courses);
        }, 1000);
    });
}

async function loadCourses() {
    grid.innerHTML = '<p style="text-align:center">Loading courses...</p>';
    const data = await fetchAllCourses();
    renderCourses(data);
}

loadCourses();

searchInput.addEventListener("input", () => {
    const searchText = searchInput.value.toLowerCase();
    const filteredCourses = courses.filter(course =>
        course.name.toLowerCase().includes(searchText)
    );
    renderCourses(filteredCourses);
});

sortButton.addEventListener("click", () => {
    courses.sort((a, b) => b.credits - a.credits);
    renderCourses(courses);
});

grid.addEventListener("click", event => {
    const card = event.target.closest(".course-card");
    if (!card) return;
    const id = Number(card.dataset.id);
    const course = courses.find(course => course.id === id);
    selectedCourse.textContent = `Selected: ${course.name} | Grade: ${course.grade}`;
});

function fetchUser(id) {
    return fetch('https://jsonplaceholder.typicode.com/users/' + id)
        .then(response => response.json())
        .then(data => {
            console.log('User name:', data.name);
            return data;
        })
        .catch(error => console.log('Error:', error));
}

fetchUser(1);

async function fetchUserAsync(id) {
    try {
        const response = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
        const data = await response.json();
        console.log('User name (async):', data.name);
        return data;
    } catch (error) {
        console.log('Error:', error);
    }
}

fetchUserAsync(1);

async function fetchTwoUsers() {
    try {
        const [user1, user2] = await Promise.all([
            fetch('https://jsonplaceholder.typicode.com/users/1').then(r => r.json()),
            fetch('https://jsonplaceholder.typicode.com/users/2').then(r => r.json())
        ]);
        console.log('User 1:', user1.name);
        console.log('User 2:', user2.name);
    } catch (error) {
        console.log('Error:', error);
    }
}

fetchTwoUsers();
const notificationsGrid = document.querySelector("#notifications-grid");
const loading = document.querySelector("#loading");
const errorMessage = document.querySelector("#error-message");
const errorText = document.querySelector("#error-text");
const retryBtn = document.querySelector("#retry-btn");

async function apiFetch(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

async function loadNotifications(url) {
    try {
        loading.style.display = 'block';
        errorMessage.style.display = 'none';
        notificationsGrid.innerHTML = '';

        const posts = await apiFetch(url);

        posts.slice(0, 5).forEach(post => {
            const card = document.createElement('div');
            card.className = 'course-card';
            card.innerHTML = `
                <h3>${post.title}</h3>
                <p>${post.body}</p>
            `;
            notificationsGrid.appendChild(card);
        });

    } catch (error) {
        errorText.textContent = `Something went wrong: ${error.message}`;
        errorMessage.style.display = 'block';
    } finally {
        loading.style.display = 'none';
    }
}

loadNotifications('https://jsonplaceholder.typicode.com/posts');

retryBtn.addEventListener('click', () => {
    loadNotifications('https://jsonplaceholder.typicode.com/posts');
});

loadNotifications('https://jsonplaceholder.typicode.com/nonexistent');

async function apiFetchAxios(url) {
    const response = await axios.get(url);
    return response.data;
}

axios.interceptors.request.use(config => {
    console.log('API call started:', config.url);
    return config;
});

async function loadPostsByUser(userId) {
    try {
        const response = await axios.get(
            'https://jsonplaceholder.typicode.com/posts',
            { params: { userId: userId } }
        );
        console.log(`Posts by user ${userId}:`, response.data);
    } catch (error) {
        console.log('Error:', error.message);
    }
}

loadPostsByUser(1);

/*
FETCH vs AXIOS -- 3 KEY DIFFERENCES:
1. JSON Parsing:
   - Fetch: manual → response.json()
   - Axios: automatic → response.data

2. Error Handling:
   - Fetch: only rejects on network errors, not 404/500
   - Axios: throws on any non-2xx response automatically

3. Features:
   - Fetch: basic, built into browser
   - Axios: interceptors, timeout, params object built in
*/