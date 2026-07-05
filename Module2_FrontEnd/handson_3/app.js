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
    (total, course) => total + course.credits,
    0
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
        (total, course) => total + course.credits,
        0
    );

    totalPara.textContent = `Total Credits: ${credits}`;

}

renderCourses(courses);

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

    selectedCourse.textContent =
        `Selected Course: ${course.name} | Grade: ${course.grade}`;

});