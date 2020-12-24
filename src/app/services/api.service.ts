import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  // Interfaces

  constructor(private http: HttpClient) { }

  API_BASE = 'http://localhost:8080/api/v1/'

  /**
   * POST request for user login
   *
   * @param payload
   */
  userLogin(payload: object) {
    return this.http.post<any>(
      this.API_BASE + 'users/login',
      payload
    ).pipe(map(this.extractData), catchError(this.errorHandler));
  };

  
  /**
   * POST request for user registration
   *
   * @param payload
   */
  userRegistration(payload: object) {
    return this.http.post<any>(
      this.API_BASE + 'users/register',
      payload
    ).pipe(map(this.extractData), catchError(this.errorHandler));
  }





  /**
   * Method for catching errors from API requests
   *
   * @param error
   */
  errorHandler(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
    // return an observable with error message
    if (typeof error.error === 'object' && error.error !== null) {
      return throwError(error.error['error']);
    }
    return throwError(
      'Something bad happened; please try again later.');
  }

  /**
   * Function to extract the data when the server return some
   *
   * @param res
   */
  private extractData(res: Response) {
    let body = res;
    return body || {};
  }

}
