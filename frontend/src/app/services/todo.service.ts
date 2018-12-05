import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Todo } from '../todo';
import { Observable, of } from 'rxjs';
import { map, tap, catchError } from 'rxjs/operators';

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
}

@Injectable({
  providedIn: 'root'
})
export class TodoService {

  constructor(private http: HttpClient) { }
  
  private todoUrl ='/api/todo/';

  getAllTodos(): Observable<Todo[]> {
    return this.http.get<Todo[]>(this.todoUrl)
      .pipe(
        catchError(this.handleError('getTodo', []))
      )
  }

  addTodo(content: string): Observable<Todo> {
    const payload = {content}
    return this.http.post<Todo>(this.todoUrl, payload, httpOptions)
      .pipe(catchError(this.handleError<Todo>('addTodo')))
  }

  updateTodo(todo: Todo): Observable<void> {
    const url = `${this.todoUrl}${todo.id}/`;
    return this.http.put(url, todo, httpOptions)
      .pipe(
        tap(_ => this.log(`updated hero id=${todo.id}`)),
        catchError(this.handleError<any>('updateTodo'))
        
      );
  }
  getTodoById(todoId: number): Observable<Todo> {
    const url = `${this.todoUrl}${todoId}/`;
    return this.http.get<Todo>(url)
      .pipe(
        catchError(this.handleError<Todo>(`getTodo id= ${todoId}`))
      )
  }

  deleteTodoById(todoId: number): Observable<void> {
    const url = `${this.todoUrl}${todoId}/`;
    return this.http.delete<void>(url, httpOptions)
      .pipe(
        catchError(this.handleError<void>('deleteTodo'))
      )
  }
  private log(message: string) {
    console.log(`TodoService: ${message}`);
  }
  private handleError<T> (operation = 'operation', result?: T ){
    return (error: any): Promise<T> => {
      console.error(error);
      this.log(`${operation} failed: ${error.message}`);

      return Promise.resolve(result as T);
    };
  }
}
