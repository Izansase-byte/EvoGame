import settings
import pygame


class Laboratory:
    def __init__(self):
        self.rect = pygame.Rect(220, 120, 560, 650)
        self.buttons = {}
        self.seed_value = None

    def handle_event(self, event, simulation):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if event.button != 1:
            return
        for action, rect in self.buttons.items():
            if rect.collidepoint(event.pos):
                self.apply(action, simulation)
                break
    
    def apply_preset(self,name, simulation):
        presets= {
            'abundance': {
                'mutation': 0.1,
                'energy': 1.0,
                'food_rate': 8.0
            },
            'scarcity': {
                'mutation': 0.1,
                'energy': 1.0,
                'food_rate': 0.5
            },
            'high_mutation': {
                'mutation': 0.3,
                'energy' : 1.0,
                'food_rate':4.0
                
            }
        }
        
        preset = presets[name]
        
        simulation.mutation_rate = preset['mutation']
        simulation.energy_multiplier = preset['energy']
        simulation.food_interval = 1 / preset['food_rate']
        simulation.food_timer = 0
        simulation.seasons_enabled = False

    
    def apply(self, action, simulation):
        if self.seed_value is None:
            self.seed_value = simulation.seed
        if action == 'seed_minus':
            self.seed_value = max(0, self.seed_value - 1)
            return
        if action == 'seed_plus':
            self.seed_value = min(999999, self.seed_value + 1)
            return
        if action == 'restart_seed':
            simulation.__init__(seed=self.seed_value)
            return

        if action.startswith('preset_'):
            self.apply_preset(action.removeprefix('preset_'), simulation)
            return

        if action == 'mutation_minus':
            simulation.mutation_rate = max(0, round(simulation.mutation_rate - 0.01, 2))
        elif action == 'mutation_plus':
            simulation.mutation_rate = min(0.30, round(simulation.mutation_rate + 0.01, 2))
        elif action == 'energy_minus':
            simulation.energy_multiplier = max(0.1, round(simulation.energy_multiplier - 0.1, 1))
        elif action == 'energy_plus':
            simulation.energy_multiplier = min(3.0, round(simulation.energy_multiplier + 0.1, 1))
        elif action == 'food_minus':
            rate = max(0.2, round(1 / simulation.food_interval - 0.2, 2))
            simulation.food_interval = 1 / rate
        elif action == 'food_plus':
            rate = min(10, round(1 / simulation.food_interval + 0.2, 2))
            simulation.food_interval = 1 / rate
        elif action == 'duration_minus':
            simulation.next_season_duration = max(10, simulation.next_season_duration - 10)
        elif action == 'duration_plus':
            simulation.next_season_duration = min(120, simulation.next_season_duration + 10)
        elif action == 'reset_values':
            simulation.mutation_rate = 0.10
            simulation.energy_multiplier = 1.0
            simulation.seasons_enabled = True
            simulation.season_duration = settings.SEASON_DURATION
            simulation.next_season_duration = settings.SEASON_DURATION
            simulation.season_timer = 0
            simulation.food_timer = 0
            simulation.food_interval = settings.SEASONS[simulation.season_index][1]
        elif action == 'toggle_seasons':
            simulation.seasons_enabled = not simulation.seasons_enabled

    def draw(self, screen, font, simulation):
        self.rect.center = screen.get_rect().center
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        pygame.draw.rect(screen, (32, 38, 48), self.rect, border_radius=12)
        self.buttons.clear()
        self.draw_text(screen, font, 'Laboratorio | Tab: cerrar', 20, 20)
        rows = [
            ('Mutación', f'{simulation.mutation_rate:.0%}', 'mutation'),
            ('Coste de energía', f'x{simulation.energy_multiplier:.1f}', 'energy'),
            ('Comida / segundo', f'{1 / simulation.food_interval:.1f}', 'food'),
            ('Próxima estación', f'{simulation.next_season_duration:.0f} s', 'duration')
        ]
        for index, (label, value, name) in enumerate(rows):
            y = self.rect.y + 70 + index * 50
            self.draw_text(screen, font, label, 20, 77 + index * 50)
            self.draw_text(screen, font, value, 290, 77 + index * 50)
            self.draw_button(screen, font, name + '_minus', '-', pygame.Rect(self.rect.x + 420, y, 40, 36))
            self.draw_button(screen, font, name + '_plus', '+', pygame.Rect(self.rect.x + 475, y, 40, 36))
        state = 'ON' if simulation.seasons_enabled else 'OFF'
        self.draw_button(screen, font, 'toggle_seasons', f'Estaciones automáticas: {state}', pygame.Rect(self.rect.x + 20, self.rect.y + 280, 520, 40))
        self.draw_button(
            screen, font, 'reset_values', 'Restaurar valores',
            pygame.Rect(self.rect.x + 20, self.rect.y + 330, 520, 40)
        )
        preset_buttons = [
            ('abundance', 'Abundancia'),
            ('scarcity', 'Escasez'),
            ('high_mutation', 'Mutación alta')
        ]
        for index, (name, label) in enumerate(preset_buttons):
            self.draw_button(
                screen, font, 'preset_' + name, label,
                pygame.Rect(self.rect.x + 20 + index * 175, self.rect.y + 390, 170, 40)
            )
        small_font = pygame.font.Font(None, 21)
        self.draw_text(screen, small_font, 'Los presets conservan la población y detienen las estaciones.', 20, 445)
        self.draw_text(screen, small_font, 'Con estaciones ON, la comida se reajusta al cambiar de estación.', 20, 470)
        if self.seed_value is None:
            self.seed_value = simulation.seed
        self.draw_text(screen, font, f'Semilla nueva: {self.seed_value}', 20, 507)
        self.draw_button(screen, font, 'seed_minus', '-', pygame.Rect(self.rect.x + 420, self.rect.y + 500, 40, 36))
        self.draw_button(screen, font, 'seed_plus', '+', pygame.Rect(self.rect.x + 475, self.rect.y + 500, 40, 36))
        self.draw_button(screen, font, 'restart_seed', 'Reiniciar con esta semilla', pygame.Rect(self.rect.x + 20, self.rect.y + 545, 520, 36))
        self.draw_text(screen, small_font, 'Reiniciar borra la población y el historial actuales.', 20, 590)
        self.draw_text(screen, small_font, 'El laboratorio pausa la simulación. Tab: cerrar.', 20, 620)

    def draw_button(self, screen, font, action, label, rect):
        self.buttons[action] = rect
        pygame.draw.rect(screen, (65, 78, 98), rect, border_radius=6)
        text = font.render(label, True, (240, 240, 240))
        screen.blit(text, text.get_rect(center=rect.center))

    def draw_text(self, screen, font, text, x, y):
        surface = font.render(text, True, (240, 240, 240))
        screen.blit(surface, (self.rect.x + x, self.rect.y + y))
