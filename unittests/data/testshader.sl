/*
   This shader is used to test the slparams module.
 */

#define arg float Kd = 0.5

surface testshader(float Ka = 1;
		   varying vector norm = 0;
		   float uv[2] = {1,2};  /* comment */
		   output point out = point "world" (0,0,0); // comment
		   uniform color col = color "rgb" (1,1,1);
		   arg;
                  )
{
#define TEST_LINE_CONTINUATION { \
}

  Cs = color "rgb" (1,1,1);
  Oi = 1;
}
