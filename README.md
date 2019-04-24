## Client application example

    Enter server address: BlaBlaBla
    Enter valid server address ("exit" to exit)
    http://[::]:5000
    Game Manager "What? Where? When?"
    Enter a command ("--help" for a list of commands, "exit" to exit)
    > create_game
    usage: client.py [-h]
                     {add_participant,add_points,show_table,get_question,get_answer,end,load_previous}
                     ...
    
    positional arguments:
      {add_participant,add_points,show_table,get_question,get_answer,end,load_previous}
        add_participant     Add one participant
        add_points          Add points to the participant
        show_table          Show game table
        get_question        Get one question from the base
        get_answer          Get the answer to the previous question
        end                 Exit game mode
        load_previous       Load previous game instead of this one (note: without
                            saving)
    
    optional arguments:
      -h, --help            show this help message and exit
    The game is running.
    >> add_participant Pavel
    Participant was added.
    >> show_table
    Pavel has 50 points
    Alexey has 150 points
    Dasha has 35 points
    Table was shown.
    >> add_points Pavel 100
    Points were added.
    >> get_question
    Why did the chicken cross the road?
    The question was shown.
    >> get_answer
    To get to the other side.
    The answer was shown.
    >> end
    Save the game? (y/n, default = y): y
    Game was saved.
    > add_package
    usage: client.py [-h] {save,add_question} ...
    
    positional arguments:
      {save,add_question}
        save               Save the package
        add_question       Add question to the package
    
    optional arguments:
      -h, --help           show this help message and exit
    Package mode is activated.
    >> add_question -t Text -a Answer
    The question was added to the package.
    >> add_question -t Text2 -a Answer2
    The question was added to the package.
    >> save
    Package was saved.
    > create_game
    usage: client.py [-h]
                     {add_participant,add_points,show_table,get_question,get_answer,end,load_previous}
                     ...
    
    positional arguments:
      {add_participant,add_points,show_table,get_question,get_answer,end,load_previous}
        add_participant     Add one participant
        add_points          Add points to the participant
        show_table          Show game table
        get_question        Get one question from the base
        get_answer          Get the answer to the previous question
        end                 Exit game mode
        load_previous       Load previous game instead of this one (note: without
                            saving)
    
    optional arguments:
      -h, --help            show this help message and exit
    The game is running.
    >> exit
    Save the game? (y/n, default = y): n
    Game wasn't saved.
    Goodbye!