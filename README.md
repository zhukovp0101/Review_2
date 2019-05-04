# Client application example
---
### Simulation of manual input using a text file containing the program:
    
    python3 client.py --address http://127.0.0.1:6000/ --program test_program.txt
    Game Manager "What? Where? When?"
    Enter a command ("--help" for a list of commands, "exit" to exit)
    > --help
    usage: client.py [-h] {load_data,add_question,add_package,create_game} ...
    
    positional arguments:
      {load_data,add_question,add_package,create_game}
        load_data           Adding packages and questions from file
        add_question        Add question to database
        add_package         Add package to database
        create_game         Create a new game
    
    optional arguments:
      -h, --help            show this help message and exit
    > load_data test_questions_data.json
    Package mode is activated; package: TestPackage_1
    --The question was added.
    --The question was added.
    --The question was added.
    Package mode is activated; package: TestPackage_2
    --The question was added.
    --The question was added.
    --The question was added.
    The question was added.
    The question was added.
    The question was added.
    Data loaded.
    > create_game
    usage: client.py [-h]
                     {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
                     ...
    
    positional arguments:
      {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
        add_participant     Add one participant
        add_points          Add points to the participant
        show_table          Show game table
        get_question        Get one question from the base
        get_package         Get one package from the base
        lost_package        Reset package game mode
        get_answer          Get the answer to the previous question
        end                 Exit game mode
        load_previous       Load last previous game (if the date and name are not
                            specified) instead of this one (note: without saving)
    
    optional arguments:
      -h, --help            show this help message and exit
    The game is running.
    >> add_participant "Becky Thatcher"
    Participant was added.
    >> add_participant Tom
    Participant was added.
    >> add_participant "Huckleberry Finn"
    Participant was added.
    >> get_question --name Anti-humor
    Package: None
    Author: 
    Complexity: 1
    Name: Anti-humor
    Question: Why did the chicken cross the road?
    The question was shown.
    >> get_answer
    To get to the other side.
    Comment: None
    The answer was shown.
    >> get_package
    Author: Tester
    Name: TestPackage_2
    Complexity: 5
    The package was found.
    >> get_question
    Package: TestPackage_2
    Author: Андрей Солдатов
    Complexity: 4
    Name: 
    Question: Персонаж Милорада Павича считал, что в мире существует устойчивый баланс: чет и нечет, правое и левое, мужское и женское. Одним из следствий этого было отвращение к некоему интеллектуальному занятию. Какому именно?
    The question was shown.
    >> get_answer
    Шахматы.
    Comment: None
    The answer was shown.
    >> add_points Tom 50
    Points were added.
    >> add_points "Becky Thatcher" 100
    Points were added.
    >> end
    Save the game?
    Game was saved.
    > create_game
    usage: client.py [-h]
                     {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
                     ...
    
    positional arguments:
      {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
        add_participant     Add one participant
        add_points          Add points to the participant
        show_table          Show game table
        get_question        Get one question from the base
        get_package         Get one package from the base
        lost_package        Reset package game mode
        get_answer          Get the answer to the previous question
        end                 Exit game mode
        load_previous       Load last previous game (if the date and name are not
                            specified) instead of this one (note: without saving)
    
    optional arguments:
      -h, --help            show this help message and exit
    The game is running.
    >> load_previous
    Previous game was loaded.
    >> show_table
    Becky Thatcher has 100 points.
    Tom has 50 points.
    Huckleberry Finn has 0 points.
    Table was shown.
    >> add_points Tom 50
    Points were added.
    >> end
    Save the game?
    Game wasn't saved.
    > create_game
    usage: client.py [-h]
                     {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
                     ...
    
    positional arguments:
      {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
        add_participant     Add one participant
        add_points          Add points to the participant
        show_table          Show game table
        get_question        Get one question from the base
        get_package         Get one package from the base
        lost_package        Reset package game mode
        get_answer          Get the answer to the previous question
        end                 Exit game mode
        load_previous       Load last previous game (if the date and name are not
                            specified) instead of this one (note: without saving)
    
    optional arguments:
      -h, --help            show this help message and exit
    The game is running.
    >> load_previous
    Previous game was loaded.
    >> show_table
    Becky Thatcher has 100 points.
    Tom has 50 points.
    Huckleberry Finn has 0 points.
    Table was shown.
    >> end
    Save the game?
    Game wasn't saved.
    > add_question -t SuperQuestion -a SuperAnswer --name Super --comment SuperComment
    The question was added.
    > create_game
    usage: client.py [-h]
                     {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
                     ...
    
    positional arguments:
      {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
        add_participant     Add one participant
        add_points          Add points to the participant
        show_table          Show game table
        get_question        Get one question from the base
        get_package         Get one package from the base
        lost_package        Reset package game mode
        get_answer          Get the answer to the previous question
        end                 Exit game mode
        load_previous       Load last previous game (if the date and name are not
                            specified) instead of this one (note: without saving)
    
    optional arguments:
      -h, --help            show this help message and exit
    The game is running.
    >> get_question --name Super
    Package: None
    Author: None
    Complexity: None
    Name: Super
    Question: SuperQuestion
    The question was shown.
    >> exit
    Save the game?
    Game was saved.
    Goodbye!
---
### Manual input:
    python3 client.py --address http://127.0.0.1:6000
    Game Manager "What? Where? When?"
    Enter a command ("--help" for a list of commands, "exit" to exit)
    > 
    > add_package MyPack
    usage: client.py [-h] {save,add_question} ...
    
    positional arguments:
      {save,add_question}
        save               Save the package
        add_question       Add question to the package
    
    optional arguments:
      -h, --help           show this help message and exit
    Package mode is activated; package: MyPack
    >> add_question -t TextQuestion -a AnsQ --author Me --name MyQuestion
    The question was added.
    >> save
    Package was saved.
    > create_game
    usage: client.py [-h]
                     {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
                     ...
    
    positional arguments:
      {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
        add_participant     Add one participant
        add_points          Add points to the participant
        show_table          Show game table
        get_question        Get one question from the base
        get_package         Get one package from the base
        lost_package        Reset package game mode
        get_answer          Get the answer to the previous question
        end                 Exit game mode
        load_previous       Load last previous game (if the date and name are not
                            specified) instead of this one (note: without saving)
    
    optional arguments:
      -h, --help            show this help message and exit
    The game is running.
    >> get_package --name MyPack
    Author: None
    Name: MyPack
    Complexity: None
    The package was found.
    >> get_question
    Package: MyPack
    Author: Me
    Complexity: None
    Name: MyQuestion
    Question: TextQuestion
    The question was shown.
    >> get_answer
    AnsQ
    Comment: None
    The answer was shown.
    >> end
    Save the game?
    y
    Game was saved.
    > create_game
    usage: client.py [-h]
                     {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
                     ...
    
    positional arguments:
      {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
        add_participant     Add one participant
        add_points          Add points to the participant
        show_table          Show game table
        get_question        Get one question from the base
        get_package         Get one package from the base
        lost_package        Reset package game mode
        get_answer          Get the answer to the previous question
        end                 Exit game mode
        load_previous       Load last previous game (if the date and name are not
                            specified) instead of this one (note: without saving)
    
    optional arguments:
      -h, --help            show this help message and exit
    The game is running.
    >> load_previous --date 2019/05/04
    Previous game was loaded.
    >> end
    Save the game?
    n
    Game wasn't saved.
    > create_game
    usage: client.py [-h]
                     {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
                     ...
    
    positional arguments:
      {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
        add_participant     Add one participant
        add_points          Add points to the participant
        show_table          Show game table
        get_question        Get one question from the base
        get_package         Get one package from the base
        lost_package        Reset package game mode
        get_answer          Get the answer to the previous question
        end                 Exit game mode
        load_previous       Load last previous game (if the date and name are not
                            specified) instead of this one (note: without saving)
    
    optional arguments:
      -h, --help            show this help message and exit
    The game is running.
    >> add_participant Pavel
    Participant was added.
    >> add_points Pavel 50
    Points were added.
    >> end
    Save the game?
    y
    Game was saved.
    > create_game
    usage: client.py [-h]
                     {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
                     ...
    
    positional arguments:
      {add_participant,add_points,show_table,get_question,get_package,lost_package,get_answer,end,load_previous}
        add_participant     Add one participant
        add_points          Add points to the participant
        show_table          Show game table
        get_question        Get one question from the base
        get_package         Get one package from the base
        lost_package        Reset package game mode
        get_answer          Get the answer to the previous question
        end                 Exit game mode
        load_previous       Load last previous game (if the date and name are not
                            specified) instead of this one (note: without saving)
    
    optional arguments:
      -h, --help            show this help message and exit
    The game is running.
    >> load_previous --date 2019/05/04
    Previous game was loaded.
    >> show_table
    Pavel has 50 points.
    Table was shown.
    >> end
    Save the game?
    n
    Game wasn't saved.
    > exit
    Goodbye!
---
### Server run:
    python3 server.py --host 127.0.0.1 --port 6000 --db_configs database_configs.json
     * Serving Flask app "What? Where? When?" (lazy loading)
     * Environment: production
       WARNING: Do not use the development server in a production environment.
       Use a production WSGI server instead.
     * Debug mode: on
     * Running on http://127.0.0.1:6000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: 580-668-707
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /package/activate HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /package/add_question HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /package/add_question HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /package/add_question HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /package/save HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /package/activate HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /package/add_question HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /package/add_question HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /package/add_question HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /package/save HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /add_question HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /add_question HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /add_question HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/activate HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/add_participant HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/add_participant HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/add_participant HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/get_question HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET /game/get_answer HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/get_package HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/get_question HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET /game/get_answer HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/add_points HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/add_points HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/save HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/activate HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/load_previous HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET /game/show_table HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/add_points HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/activate HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/load_previous HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET /game/show_table HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /add_question HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/activate HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/get_question HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "GET / HTTP/1.1" 200 -
    127.0.0.1 - - [04/May/2019 16:11:51] "POST /game/save HTTP/1.1" 200 -