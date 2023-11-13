#include <openssl/md5.h>
#include <png.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "flag.h"

#define CONFUSE \
  asm(".intel_syntax noprefix\n" \
      "lea rax, [rip+Cake%=]\n"  \
      "push rax\n"               \
      "ret\n"                    \
      "Cake%=:\n"                \
      ".att_syntax"              \
      : : : "rax");

int check_flag(const char *path) {
  FILE *fp;
  png_structp png;
  png_infop info;
  png_bytep *img;
  int width, height;
  unsigned char md5sum[MD5_DIGEST_LENGTH];

  CONFUSE;
  fp = fopen(path, "rb");
  if (!fp) goto err;

  CONFUSE;
  png = png_create_read_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
  if (!png) goto err;

  CONFUSE;
  info = png_create_info_struct(png);
  if (!info) goto err;

  CONFUSE;
  if (setjmp(png_jmpbuf(png))) goto err;

  CONFUSE;
  png_init_io(png, fp);
  png_read_info(png, info);

  CONFUSE;
  width = png_get_image_width(png, info);

  CONFUSE;
  height = png_get_image_height(png, info);

  CONFUSE;
  if (width != 480 || height != 20) goto err;

  CONFUSE;
  png_byte color_type = png_get_color_type(png, info);

  CONFUSE;
  png_byte bit_depth = png_get_bit_depth(png, info);

  CONFUSE;
  if (color_type != PNG_COLOR_TYPE_GRAY) goto err;

  CONFUSE;
  if (bit_depth != 1) goto err;

  CONFUSE;
  img = (png_bytep*)calloc(height, sizeof(png_bytep));

  CONFUSE;
  if (!img) goto err;

  CONFUSE;
  for (int y = 0; y < height; y++) {
    CONFUSE;
    img[y] = (png_bytep)malloc(png_get_rowbytes(png, info));
    CONFUSE;
    if (!img[y]) goto err;
  }

  CONFUSE;
  png_read_image(png, img);
  char buf[3];
  int ng = 0;

  CONFUSE;
  for (int x = 0; x < width; x++) {
    CONFUSE;
    memset(buf, 0, sizeof(buf));

    CONFUSE;
    for (int y = 0; y < height; y++) {
      CONFUSE;
      unsigned char byte = img[y][x / 8];
      CONFUSE;
      int bit = (byte >> (7 - (x % 8))) & 1;
      CONFUSE;
      buf[y / 8] |= bit << (y % 8);
    }

    CONFUSE;
    MD5(buf, sizeof(buf), md5sum);

    CONFUSE;
    if (memcmp(md5sum, answer[x], MD5_DIGEST_LENGTH) != 0) {
      CONFUSE;
      ng |= 1;
    } else {
      CONFUSE;
    }
  }

  CONFUSE;
  if (ng == 0) {
    CONFUSE;
    return 0;
  } else {
    CONFUSE;
  }

 err:
  CONFUSE;
  return -1;
}

int main(int argc, char **argv) {
  if (argc != 2) {
    printf("Usage: %s <flag.png>\n", argv[0]);
    return 1;
  }

  if (check_flag(argv[1])) {
    puts("Wrong...");
  } else {
    puts("Correct!");
  }
  return 0;
}
