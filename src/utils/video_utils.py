import cv2
import imageio
def save_video(output_video_frames,output_video_path_avi, output_video_path_mp4):
    if not output_video_frames:
        print("No frames to save.")
        return

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    height, width = output_video_frames[0].shape[:2]
    out = cv2.VideoWriter(output_video_path_avi, fourcc, 60, (width, height))

    for frame in output_video_frames:
        out.write(frame)
    out.release()


    reader = imageio.get_reader(output_video_path_avi)
    writer = imageio.get_writer(output_video_path_mp4, fps=30) 
    for frame in reader:
        writer.append_data(frame)
    writer.close()

    #print(f"Video saved in: {output_video_path}")
