# Architecture

## Structure

*GameLoop* class runs the game loop and utilizes the classes *Renderer*, *EventQueue*, *Clock*, *ArrowKeys* and *Game*. The game logic is contained in the *Game* class. These relationships between the classes are depicted below:

```mermaid
classDiagram
    GameLoop "1" -- "1" Game
    Game "1" -- "1" Background
    pygame.sprite.Sprite <|-- Background
    Game "1" -- "*" Character
    GameLoop "1" -- "1" Renderer
    GameLoop "1" -- "1" EventQueue
    GameLoop "1" -- "1" Clock
    GameLoop "1" -- "1" ArrowKeys
    class GameLoop{
        start()
    }
    class Game{
        player
        enemies
        finished
        draw()
        update()
    }
    class Renderer{
        render()
    }
    class EventQueue{
        get()
    }
    class Clock{
        tick()
    }
    class ArrowKeys{
        current_direction
        handle(event)
        release_all()
    }
```

The game character logic is contained in the *Character* class. The directional data of the character is handled by the *CharacterDirection* class, the animations are handled by the *AnimationsComponent* class, and the character movement and collision detection is handled by the *PhysicsComponent* class. The state transitions of the character (*idle* -> *walking* -> *attacking* etc.) are handled by the subclasses of the *State* class (player states are inside the *states* directory and enemy states inside the *ai* directory). All these relationships are depicted below:

```mermaid
classDiagram
    Game "1" -- "*" Character
    Character "1" -- "1" State
    State <|-- states.SomeState
    State <|-- ai.SomeState
    Character "1" -- "1" CharacterDirection
    CharacterDirection "1" -- "*" Direction
    CharacterDirection <|-- PlayerDirection
    Character "1" -- "1" AnimationsComponent
    Character "1" -- "1" PhysicsComponent
    PhysicsComponent <|-- PlayerPhysics
    class Game{
    }
    class Character{
        sprite
        has_been_defeated
        update()
        handle_event()
        does_attack_hit()
        defeat()
    }
    class State{
        type
        enter()
        update()
        handle_event()
    }
    class states.SomeState{
        type
        enter()
        update()
        handle_event()
    }
    class ai.SomeState{
        type
        enter()
        update()
        handle_event()
    }
    class CharacterDirection{
        facing
        moving
        handle(event)
    }
    class Direction{
        vertical_component
        horizontal_component
        movement_vector()
        clip_to_four_directions()
    }
    class PlayerDirection{
        facing
        moving
        controlled_toward
        handle(event)
    }
    class AnimationsComponent{
        update()
        current_frame()
        reset()
    }
    class PhysicsComponent{
        bounding_box
        update()
        does_attack_hit()
    }
    class PlayerPhysics{
        bounding_box
        update()
        does_attack_hit()
    }
```

## Game logic

### Game loop

The basic function of the game loop is presented as a sequence diagram below. The diagram includes the initialization of the game loop and one iteration. Animation states and AI states are excluded from the diagram.

```mermaid
sequenceDiagram
    create participant main
    create participant game
    main->>game: Game()
    create participant background
    game->>background: Background()
    create participant player
    game->>player: Character("player", initial_state, starting_position, direction, animations, physics)
    create participant enemy
    game->>enemy: Character("enemy", initial_state, starting_position, direction, animations, physics)
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
    game_loop->>game: handle(event)
    game->>player: handle(event, enemies)
    player-->>game: 
    game-->>game_loop: 
    game_loop->>game: update(dt)
    game->>player: update(dt, opponents_to)
    player-->>game: 
    game->>enemy: update(dt, opponents_to)
    enemy-->>game: 
    game-->>game_loop: 
    game_loop->>renderer: render()
    renderer->>game: draw(intermediate_surface)
    game-->>renderer: 
    renderer-->>game_loop: 
    game_loop->>clock: tick(60)
    clock-->>game_loop: dt
```

### Player and AI states

The initial state of the game character is passed to the *Character* constructor in the *initial_state* parameter (for a player character the initial state is usually *states.idle_state.IdleState()* and for an enemy character *ai.idle_state.IdleState()*). The *update()* method of the current state is called each game loop iteration and the *handle_event()* method of the state when another game component sends a game event to the character (e.g. the *Game* object sends a *PlayerWon* event).

Both the *update()* method and the *handle_event()* either return another state or *None*. When they return another state, the character will change its current state to that state. So for example if the player character's current state is *IdleState* and it receives the *AttackStarted* event in its *handle_event()* method, then the *handle_event()* method would return an *AttackState* and the player character would change its state to that state.

The *enter()* method of a state is called the first thing when a character has changed its current state to that state. It does any preparatory tasks required by the state such as update the movement direction of the character if the new state is a *WalkState*.
