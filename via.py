import pyspiel


_NUM_PLAYERS = 2
_NUM_COLS = 6
_NUM_CELLS = _NUM_COLS**2
_GAME_TYPE = pyspiel.GameType(
    short_name="via",
    long_name="via: route finding strategy",
    dynamics=pyspiel.GameType.Dynamics.SEQUENTIAL,
    chance_mode=pyspiel.GameType.ChanceMode.DETERMINISTIC,
    information=pyspiel.GameType.Information.PERFECT_INFORMATION,
    utility=pyspiel.GameType.Utility.ZERO_SUM,
    reward_model=pyspiel.GameType.RewardModel.TERMINAL,
    max_num_players=_NUM_PLAYERS,
    min_num_players=_NUM_PLAYERS,
    provides_information_state_string=True,
    provides_information_state_tensor=False,
    provides_observation_string=False,
    provides_observation_tensor=False,
    parameter_specification={})
_GAME_INFO = pyspiel.GameInfo(
    num_distinct_actions=_NUM_CELLS,
    max_chance_outcomes=0,
    num_players=2,
    min_utility=-1.0,
    max_utility=1.0,
    utility_sum=0.0,
    max_game_length=_NUM_CELLS)


class ViaGame(pyspiel.Game):
    def __init__(self, params=None):
        super().__init__(_GAME_TYPE, _GAME_INFO, params or dict())

    def new_initial_state(self):
        return ViaState(self)


class ViaState(pyspiel.State):
    def __init__(self, game):
        super().__init__(game)
        n            = _NUM_COLS
        self._term   = False
        self._draw   = False
        self._player = 0
        self._turn   = 0
        self._state  = [0] * _NUM_CELLS
        self._top    = set(range(n))
        self._bottom = set(range(n * (n-1), n*n))
        self._left   = set(i for i in range(n*n) if i % n == 0)
        self._right  = set(i + n -1 for i in range(n*n) if i % n == 0)

    def current_player(self):
        return self._player

    def _legal_actions(self, player):
        return [i for i,x in enumerate(self._state) if x == 0]

    def _apply_action(self, x):
        v              = 1 if self._player == 1 else -1
        self._turn    += 1
        self._state[x] = v

        top    = set(i for i in self._top if self._state[i] == v)
        bottom = set(i for i in self._bottom if self._state[i] == v)
        left   = set(i for i in self._left if self._state[i] == v)
        right  = set(i for i in self._right if self._state[i] == v)

        if self._turn == _NUM_CELLS:
            self._term = self._draw = True
        elif self._turn < -1 + _NUM_COLS * 2:
            self._term = False
        elif len(top) > 0 and len(bottom) > 0 \
           and self._is_connected(top, bottom):
            self._term = True
        elif len(left) > 0 and len(right) > 0 \
           and self._is_connected(left, right):
            self._term = True

        if not self._term:
            self._player = 1 if self._player == 0 else 0

    def is_terminal(self):
        return self._term

    def returns(self):
        if self._draw:
            mx0, mx1 = self._max_connect(0), self._max_connect(1)
            if mx0 == mx1:
                return [0.0, 0.0]
            return [1.0, -1.0] if mx0 > mx1 else [-1.0, 1.0]
        
        return [1.0, -1.0] if self._player==0 else [-1.0, 1.0]

    def _action_to_string(self, player, action):
        return f"player: {player}, move {action}"

    def __str__(self):
        a = self._state
        s = "  " + " ".join(str(i) for i in range(1, _NUM_COLS+1)) + "\n"
        for i in range(_NUM_COLS):
            row = a[i*_NUM_COLS:(i+1)*_NUM_COLS]
            s += f"{i+1} "
            for x in row:
                if x == 1: s += "\033[97m█\033[0m "
                elif x == -1: s += "\033[90m█\033[0m "
                else: s += "· "
            s += "\n"
        return s

    def _neighbours(self, x, n=_NUM_COLS):
        r,c = self.to_2d(x)
        v   = self._state[x]
        return set(self.to_1d(r,c) \
                   for r,c in ((r+1,c), (r-1,c), (r,c-1), (r,c+1)) \
                   if 1 <= r <= n and 1 <= c <= n \
                   and self._state[self.to_1d(r,c)] == v)

    def _dfs(self, Xs):
        Vs, S = set(), []
        S    += Xs
        while len(S) > 0:
            y  = S.pop()
            Ns = self._neighbours(y) - Vs
            S += Ns
            Vs.add(y); Vs.update(Ns)
        return Vs

    def _max_connect(self, player):
        x  = 1 if player == 1 else -1
        Xs = set(i for i,v in enumerate(self._state) if v==x)
        mx = 0
        while len(Xs) > 0:
            y  = Xs.pop()
            xs = self._dfs([y])
            mx = max(mx, len(xs))
            Xs = Xs - xs
        return mx
    
    def _is_connected(self, source, sink):
        Vs, S  = set(), []   
        S     += source

        while len(S) > 0:
            x = S.pop()
            if x in sink:
                return True
            Ns = self._neighbours(x) - Vs
            S += Ns
            Vs.add(x)
            Vs.update(Ns)

        return False

    def to_1d(self, r, c, n=_NUM_COLS):
        return (r-1)*n + (c-1)

    def to_2d(self, i, n=_NUM_COLS):
        return (i//n + 1, i % n + 1)

pyspiel.register_game(_GAME_TYPE, ViaGame)
