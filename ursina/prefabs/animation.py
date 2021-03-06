from ursina import *


class Animation(Sprite):
    def __init__(self, name, fps=12, loop=True, autoplay=True, frame_times=None, **kwargs):
        super().__init__()

        texture_folders = (application.compressed_textures_folder, application.asset_folder, application.internal_textures_folder)
        self.frames = [Texture(e) for e in find_sequence(name, ('png', 'jpg'), texture_folders)]
        if self.frames:
            self.texture = self.frames[0]

        self.sequence = Sequence(loop=loop, auto_destroy=False)
        for i, frame in enumerate(self.frames):
            self.sequence.append(Func(setattr, self, 'texture', self.frames[i]))
            self.sequence.append(Wait(1/fps))

        self.is_playing = False
        self.autoplay = autoplay


        for key, value in kwargs.items():
            setattr(self, key ,value)


        if self.autoplay:
            self.start()


    def start(self):
        if self.is_playing:
            self.finish()
        self.sequence.start()
        self.is_playing = True

    def pause(self):
        self.sequence.pause()

    def resume(self):
        self.sequence.resume()

    def finish(self):
        self.sequence.finish()
        self.is_playing = False


    @property
    def duration(self):
        return self.sequence.duration


    def __setattr__(self, name, value):
        if hasattr(self, 'frames') and name in ('color', 'origin'):
            for f in self.frames:
                setattr(f, name, value)

        if name == 'loop':
            self.sequence.loop = value

        try:
            super().__setattr__(name, value)
        except Exception as e:
            return e






if __name__ == '__main__':
    application.asset_folder = application.asset_folder.parent.parent / 'samples'
    app = Ursina()

    '''
    Loads an image sequence as a frame animation.
    So if you have some frames named image_000.png, image_001.png, image_002.png and so on,
    you can load it like this: Animation('image')
    '''

    Animation('ursina_wink')

    app.run()
