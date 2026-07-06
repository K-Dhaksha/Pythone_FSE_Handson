import { Component } from '@angular/core';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';
import { NgIf } from '@angular/common';

@Component({
    selector: 'app-student-profile',
    standalone: true,
    imports: [ReactiveFormsModule, NgIf],
    templateUrl: './student-profile.html',
    styleUrl: './student-profile.css'
})
export class StudentProfile {
    profileForm = new FormGroup({
        name: new FormControl('', [Validators.required]),
        email: new FormControl('', [Validators.required, Validators.email]),
        semester: new FormControl('', [
            Validators.required,
            Validators.min(1),
            Validators.max(8)
        ])
    });

    onSubmit() {
        if (this.profileForm.valid) {
            console.log(this.profileForm.value);
        }
    }
}