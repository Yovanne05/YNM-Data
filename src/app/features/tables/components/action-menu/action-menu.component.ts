import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-action-menu',
  standalone: true,
  templateUrl: './action-menu.component.html',
  styleUrls: ['./action-menu.component.scss']
})
export class ActionMenuComponent {
  @Output() edit = new EventEmitter<void>();
  @Output() delete = new EventEmitter<void>();
  isOpen = false;

  toggleMenu() {
    this.isOpen = !this.isOpen;
  }
}
