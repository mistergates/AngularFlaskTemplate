import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  API_BASE = 'http://localhost:8080/api/v1/'

  constructor(private http: HttpClient) { }

  ensureAuthenticated(token: string): Promise<any> {
    let url: string = `${this.API_BASE}/users/status`;
    let headers: HttpHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    })
    return this.http.get(url, { headers: headers }).toPromise();
  }
}
