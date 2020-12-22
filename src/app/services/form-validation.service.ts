import { Injectable } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Injectable({
  providedIn: 'root'
})
export class FormValidationService {
  form: any;

  constructor() { }

  public setForm(form: any) {
    this.form = form;
  }

  get f() {
    return this.form.controls;
  }

  public validateEmail() {
    if (this.f.email.hasError('required')) {
      return 'Email is required.';
    }
    return this.f.email.hasError('email') ? 'Not a valid email' : '';
  }

  public validatePassword() {
    return this.f.password.hasError('required') ? 'Password is required.' : '';
  }

  public validateConfirmPassword() {
    if (this.f.confirmPassword.hasError('required')) {
      return 'Password confirmation is required.';
    }
    return this.f.confirmPassword.hasError('confirmedValidator') ? 'Passwords do not match' : '';
  }

  public ConfirmedValidator(controlName: string, matchingControlName: string) {
    return (formGroup: FormGroup) => {
      const control = formGroup.controls[controlName];
      const matchingControl = formGroup.controls[matchingControlName];
      if (matchingControl.errors && !matchingControl.errors.confirmedValidator) {
        return;
      }
      if (control.value !== matchingControl.value) {
        matchingControl.setErrors({ confirmedValidator: true });
      } else {
        matchingControl.setErrors(null);
      }
    }

  }
}
