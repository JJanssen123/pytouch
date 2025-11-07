import selectors, evdev, sys
from evdev import ecodes

# === Constanten & Instellingen ===
# Minimale druk die als 'touch' telt. 0 is te laag voor jouw scherm (gebruikt 0 voor 'los'), 
# dus we kiezen een veilige, lage drempel.
DRUK_DREMPEL = 0

# === Touch Handler Klasse ===
class TouchHandler:
    def __init__(self, device_path, screen_width, screen_height, swipe_threshold=50):
        self.device_path = device_path
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.swipe_threshold = swipe_threshold # Minimale beweging (pixels) voor een swipe
        self.dev = None
        self.selector = None
        
        self.start_x = 0 # Beginpunt van de aanraking
        self.start_y = 0
        self.current_x = 0
        self.current_y = 0
        self.is_touching = False
        self.swipe_direction = None # Slaat de swipe richting op (None, 'up', 'down', etc.)
        
        self._init_device()

    def _init_device(self):
        try:
            self.dev = evdev.InputDevice(self.device_path)
            self.selector = selectors.DefaultSelector()
            self.selector.register(self.dev, selectors.EVENT_READ)
            print(f"Touchscreen initialisatie succesvol op {self.device_path}")
        except FileNotFoundError:
            print(f"Fout: Apparaat niet gevonden op {self.device_path}.")
            sys.exit(1)

    def _map_range_clamped(self, value, input_min, input_max, output_min, output_max):
        """Privé methode: Mapt een getal en houdt het binnen de grenzen."""
        mapped = output_min + ((value - input_min) / (input_max - input_min)) * (output_max - output_min)
        actual_min = min(output_min, output_max)
        actual_max = max(output_min, output_max)
        return max(actual_min, min(actual_max, mapped))

    def process_events(self):
        """Leest events, werkt de interne staat bij en controleert op het einde van een swipe."""
        self.swipe_direction = None # Reset de swipe richting aan het begin van elke frame

        for key, mask in self.selector.select(timeout=0):
            for ev in self.dev.read():
                if ev.type == ecodes.EV_ABS and ev.code == ecodes.ABS_X:
                    self.current_x = int(self._map_range_clamped(ev.value, 3600, 600, 0, self.screen_width))
                elif ev.type == ecodes.EV_ABS and ev.code == ecodes.ABS_Y:
                    self.current_y = int(self._map_range_clamped(ev.value, 3700, 240, 0, self.screen_height))
                elif ev.type == ecodes.EV_ABS and ev.code == ecodes.ABS_PRESSURE:
                    # Gebruik '>' om 0 correct als 'losgelaten' te zien
                    new_status = ev.value > DRUK_DREMPEL 
                    
                    if new_status and not self.is_touching:
                        # Start van een nieuwe aanraking
                        self.start_x = self.current_x
                        self.start_y = self.current_y
                    elif not new_status and self.is_touching:
                        # Einde van de aanraking: controleer de swipe
                        self._check_for_swipe()
                        # Reset startpunten na swipe check
                        self.start_x, self.start_y = 0, 0
                        
                    self.is_touching = new_status
                
                elif ev.type == ecodes.EV_SYN:
                    pass
    
    def _check_for_swipe(self):
        """Berekent de swipe richting wanneer de vinger wordt opgetild."""
        dx = self.current_x - self.start_x
        dy = self.current_y - self.start_y
        
        # Controleer of de beweging groter was dan de drempel
        if abs(dx) > self.swipe_threshold or abs(dy) > self.swipe_threshold:
            if abs(dx) > abs(dy):
                self.swipe_direction = 'left' if dx < 0 else 'right'
            else:
                self.swipe_direction = 'up' if dy < 0 else 'down'
