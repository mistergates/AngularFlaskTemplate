import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { FormValidationService } from '../../services/form-validation.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(
    private api: ApiService,
    private fb: FormBuilder,
    public fv: FormValidationService,
    private _snackBar: MatSnackBar,
    private router: Router) { 
      interface User {
        auth_token: string;
      }
    }

  loginForm = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required]]
  })

  ngOnInit(): void {
    // Register this form with FormValidationService
    this.fv.setForm(this.loginForm);
  }


  /**
   * Submit the user login form
   */
  submitLogin() {
    // Validate the form, return if it fails
    if (!this.loginForm.valid) {
      this._snackBar.open('Login failed.', 'Close', {
        duration: 2000,
      });
      return;
    }

    let payload = {
      email: this.fv.f.email.value,
      password: this.fv.f.password.value
    }
    console.log(payload);

    // Send payload to userLogin API
    this.api.userLogin(payload).subscribe((data: any) => {
        console.log('RECEIVED DATA:', data);
        this._snackBar.open('Login Successful.', 'Close', {
          duration: 2000,
        });
        
        // Save token to local storage
        localStorage.setItem('token', data.auth_token)
        this.router.navigate(['/']);
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
