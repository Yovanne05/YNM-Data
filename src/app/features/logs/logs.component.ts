import { Component, OnInit } from '@angular/core';
import { LogService } from '../../services/transactional/log.service.service';
import { CommonModule } from '@angular/common';

interface Log {
  timestamp: string;
  message: string;
}

@Component({
  selector: 'app-log',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './logs.component.html',
  styleUrls: ['./logs.component.scss']
})
export class LogComponent implements OnInit {
  logs: Log[] = [];

  constructor(private logService: LogService) {}

  ngOnInit(): void {
    this.loadLogs();
  }

  loadLogs(): void {
    this.logService.getLogs().subscribe({
      next: (response) => {
        this.logs = response.logs.map(log => ({
          timestamp: log[0],
          message: log[1]
        }));
      },
      error: (err) => console.error('Erreur lors du chargement des logs:', err)
    });
  }

  clearLogs(): void {
    this.logService.clearLogs().subscribe({
      next: () => {
        this.logs = [];
      },
      error: (err) => console.error('Erreur lors de la suppression des logs:', err)
    });
  }

  formatTimestamp(timestamp: string): string {
    return new Date(timestamp).toLocaleString();
  }

  isServiceMessage(message: string): boolean {
    // Adaptez cette logique selon vos besoins
    return message.startsWith('[SERVICE]') || 
           message.startsWith('[SYSTEM]') ||
           message.toLowerCase().includes('error');
  }
}