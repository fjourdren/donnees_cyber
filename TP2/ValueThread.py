from threading import Thread


class ValueThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._return = None

    def run(self):
        """
        Override de la fonction run, ajout d'une valeur de retour
        """
        if self._target:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args, **kwargs):
        """
        Override de la fonction join de la classe parente Thread
        Rajoute une valeur de retour après l'exécution normale (fin du thread).
        """
        super().join(*args, **kwargs)
        return self._return