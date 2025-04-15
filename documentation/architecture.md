# Architecture description

## Structure

```mermaid
classDiagram
    GameLoop "1" -- "1" Game
    Game "1" -- "1" Player
    Game "1" -- "*" Enemy
    Game "1" -- "1" Background
    pygame.sprite.Sprite <|-- Player
    pygame.sprite.Sprite <|-- Enemy
    pygame.sprite.Sprite <|-- Background
    class GameLoop{
        start()
    }
    class Game{
        finished
        draw()
        update()
        walk()
        attack()
    }
    class Player{
        bounding_box
        has_been_defeated
        walk()
        attack()
        lose()
    }
    class Enemy{
        bounding_box
    }
```

## Game loop

The basic function of the game loop is presented as a sequence diagram below. The diagram includes the initialization of the game loop and one iteration. Animation states and AI states are excluded from the diagram.

```mermaid
sequenceDiagram
    create participant main
    create participant game
    main->>game: Game()
    create participant background
    game->>background: Background()
    create participant player
    game->>player: Player(animations)
    create participant enemy
    game->>enemy: Enemy(animations)
    create participant renderer
    main->>renderer: Renderer(display, game, GRAPHICS_SCALING_FACTOR)
    create participant event_queue
    main->>event_queue: EventQueue()
    create participant clock
    main->>clock: Clock()
    create participant game_loop
    main->>game_loop: GameLoop(game, renderer, event_queue, clock)
    create participant arrow_keys
    game_loop->>arrow_keys: ArrowKeys()
    main->>game_loop: start()
    game_loop->>event_queue: get()
    event_queue-->>game_loop: event
    game_loop->>arrow_keys: handle(event)
    arrow_keys-->>game_loop: 
    game_loop->>game: handle_input(event, arrow_keys.current_direction)
    game->>player: handle_input(event, arrow_keys.current_direction, enemy)
    player-->>game: 
    game-->>game_loop: 
    game_loop->>game: update(dt)
    game->>player: update(dt, player, enemy)
    player-->>game: 
    game->>enemy: update(dt, player, enemy)
    enemy-->>game: 
    game-->>game_loop: 
    game_loop->>renderer: render()
    renderer->>game: draw(intermediate_surface)
    game-->>renderer: 
    renderer-->>game_loop: 
    game_loop->>clock: tick(60)
    clock-->>game_loop: dt
```
