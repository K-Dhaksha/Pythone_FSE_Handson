import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgFor, NgIf } from '@angular/common';
import { CourseCard } from '../course-card/course-card';
import { CourseService } from '../course';

@Component({
    selector: 'app-course-list',
    standalone: true,
    imports: [FormsModule, NgFor, NgIf, CourseCard],
    templateUrl: './course-list.html',
    styleUrl: './course-list.css'
})
export class CourseList implements OnInit {
    searchTerm: string = '';
    loading: boolean = true;
    courses: any[] = [];

    constructor(private courseService: CourseService) {}

    ngOnInit() {
        this.courseService.getCourses().subscribe({
            next: (data) => {
                this.courses = data.map((post: any, index: number) => ({
                    id: post.id,
                    name: post.title.slice(0, 30),
                    code: `CS10${index + 1}`,
                    credits: index % 2 === 0 ? 4 : 3,
                    grade: ['A', 'B', 'C', 'A', 'B'][index]
                }));
                this.loading = false;
            },
            error: (err) => {
                console.log(err);
                this.loading = false;
            }
        });
    }

    get filteredCourses() {
        return this.courses.filter(course =>
            course.name.toLowerCase().includes(this.searchTerm.toLowerCase())
        );
    }
}