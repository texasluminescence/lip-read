// Helper function to pick files on web platform
export const pickVideoFromLibrary = (): Promise<string> => {
  return new Promise((resolve, reject) => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'video/*';
    
    input.onchange = (event) => {
      const target = event.target as HTMLInputElement;
      const files = target.files;
      
      if (files && files.length > 0) {
        const url = URL.createObjectURL(files[0]);
        resolve(url);
      } else {
        reject(new Error('No file selected'));
      }
    };
    
    input.click();
  });
};