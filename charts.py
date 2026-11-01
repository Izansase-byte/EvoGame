import pygame

def draw_population_chart(screen, history, font, metric='population',title='Population'):
    if len(history) < 2:
        return
    
    width = 320
    height = 160
    
    panel = pygame.Surface((width, height), pygame.SRCALPHA)
    
    panel.fill((20, 25, 30, 190))
    
    title_surface = font.render(title, True, (240, 240, 240))
    panel.blit(title_surface, (10,8))
    
    left = 40
    right = width - 10
    top = 40
    bottom = height - 25
    
    samples = history[-120:]
    
    start_time = samples[0]['time']
    end_time = samples[-1]['time']
    duration = end_time - start_time
    if duration <= 0:
        return

    values = [
        sample[metric]
        for sample in samples
        if sample[metric] is not None
    ]
    
    max_value=max(1,max(values, default=1))
    
    pygame.draw.line(
        panel, (140, 140, 140), (left,top), (left, bottom)
    )
    
    pygame.draw.line(
        panel, (140, 140, 140), (left,bottom), (right, bottom)
    )
    
    season_colors = {
        'Primavera': (100, 220, 120),
        'Verano': (240, 210, 80),
        'Otoño': (220, 140, 80),
        'Invierno': (120, 180, 250)
    }
    
    small_font = pygame.font.Font(None, 18)
    previous_season = samples[0].get('season')
    
    for sample in samples[1:]:
        season = sample.get('season')
        
        if season is not None and season != previous_season:
            x = round(
                left
                + (sample['time'] - start_time)
                / duration * (right - left)
            )
            
            color = season_colors.get(season, (180, 180, 180))
            
            pygame.draw.line(
                panel, color, (x, top), (x, bottom), 1
            )
            
            label = small_font.render(season, True, color)
            
            label_x = max(
                0,
                min(x + 3, width - label.get_width() - 3)
            )
            panel.blit(label, (label_x, top - 15))
        
        previous_season = season
        
    points = []

    for sample in samples:
        value = sample[metric]

        if value is None:
            if len(points) >= 2:
                pygame.draw.lines(panel, (80, 200, 120), False, points, 2)
            points = []
            continue

        x = left + (
            (sample['time'] - start_time) / duration
        ) * (right - left)
        y = bottom - (value / max_value) * (bottom - top)
        points.append((round(x), round(y)))

    if len(points) >= 2:
        pygame.draw.lines(panel, (80, 200, 120), False, points, 2)

    maximum_label = font.render(
        f"{max_value:.1f}", True, (200, 200, 200)
    )
    panel.blit(maximum_label, (5, top))
    
    zero_label = font.render('0', True, (200,200,200))
    panel.blit(zero_label, (20, bottom - 12))
    
    time_label = font.render(
        f'{start_time:.0f}-{end_time:.0f} s',
        True,
        (200,200,200)
    )
    panel.blit(time_label, (left, bottom + 3))
    
    screen.blit(
        panel,
        (screen.get_width() - width - 10,
         screen.get_height() - height - 10
         )
    )