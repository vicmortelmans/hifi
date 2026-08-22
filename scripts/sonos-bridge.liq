source = mksafe(input.pulseaudio(
  device="alsa_input.usb-Generic_USB_Microphone_IM10000001-00.analog-stereo"
))

output.harbor(
  %mp3(bitrate=128),
  port=8040,
  mount="amp",
  source
)
