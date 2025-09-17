import tpg

displu=tpg.display()

displu.box(15, 11, 1, 1,blok='@')

displu.box(15, 11, 22, 1, filling=True)

displu.cursor(3,3 ,symbol='hi')

displu.echo(end='\n')