import { Component, EventEmitter, Output, HostListener } from '@angular/core';
import {MatIconModule} from "@angular/material/icon";

@Component({
  selector: 'app-action-menu',
  standalone: true,
  templateUrl: './action-menu.component.html',
  styleUrls: ['./action-menu.component.scss'],
  imports: [MatIconModule]
})
export class ActionMenuComponent {
  @Output() edit = new EventEmitter<void>();
  @Output() delete = new EventEmitter<void>();
  isOpen = false;

  toggleMenu() {
    this.isOpen = !this.isOpen;
  }

  isNearBottom(): boolean {
    if (typeof window === 'undefined') return false;

    const button = document.activeElement as HTMLElement;
    if (!button) return false;

    const buttonRect = button.getBoundingClientRect();
    const spaceBelow = window.innerHeight - buttonRect.bottom;

    return spaceBelow < 350;
  }
}
