import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { FormValidationService } from '../../services/form-validation.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  constructor(
    private api: ApiService,
    private fb: FormBuilder,
    public fv: FormValidationService,
    private _snackBar: MatSnackBar,
    private router: Router) { }

  registrationForm = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required]],
    confirmPassword: ['', [Validators.required]]
  }, {
    validator: this.fv.ConfirmedValidator('password', 'confirmPassword')
  })

  ngOnInit() {
    // Register this form with FormValidationService
    this.fv.setForm(this.registrationForm);
  }

  /**
   * Submit the user registration form
   */
  submitRegistration() {
    // Validate the form, return if it fails
    if (!this.registrationForm.valid) {
      this._snackBar.open('Registration failed.', 'Close', {
        duration: 2000,
      });
      return;
    }

    let payload = {
      email: this.fv.f.email.value,
      password: this.fv.f.password.value
    }
    console.log(payload);

    // Send payload to userRegistration API
    this.api.userRegistration(payload).subscribe(
      data => {
        console.log(data);
        this._snackBar.open('Registration Successful.', 'Close', {
          duration: 5000,
        });
        this.router.navigate(['/login']);
      },
      err => {
        console.log(err);
        this._snackBar.open(err, 'Close', {
          duration: 5000,
        });
      }
    );

  }

}
