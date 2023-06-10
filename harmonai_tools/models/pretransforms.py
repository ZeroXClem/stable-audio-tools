from torch import nn

class Pretransform(nn.Module):
    def __init__(self, enable_grad=False):
        super().__init__()

        self.downsampling_ratio = None

        self.enable_grad = enable_grad

    def encode(self, x):
        return x

    def decode(self, z):
        return z

class AutoencoderPretransform(Pretransform):
    def __init__(self, model):
        super().__init__()
        self.model = model

        self.downsampling_ratio = model.downsampling_ratio
    
    def encode(self, x):
        return self.model.encode(x)

    def decode(self, z):
        return self.model.decode(z)
    
    def load_state_dict(self, state_dict, strict=True):
        self.model.load_state_dict(state_dict, strict=strict)

class WaveletPretransform(Pretransform):
    def __init__(self, channels, levels, wavelet):
        super().__init__()

        from .wavelets import WaveletEncode1d, WaveletDecode1d

        self.encoder = WaveletEncode1d(channels, levels, wavelet)
        self.decoder = WaveletDecode1d(channels, levels, wavelet)

        self.downsampling_ratio = 2 ** levels
    
    def encode(self, x):
        return self.encoder(x)
    
    def decode(self, z):
        return self.decoder(z)
    