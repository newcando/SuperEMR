;
module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    clean: {
      build: {
        src: ["./build/*"]
      },
      demo: {
        src: [
          "./demo/widget/**/*",
          "./demo/widget/**"
        ]
      },
      release:{
        src:["./dist/*"]
      },
      temp:{
        src:['./temp']
      }
    },

    copy: {
      demo: {
        files: [
          {
            expand: true,
            cwd: "./build/",
            src: "./**",
            dest: "./demo/widget/"
          },
          {
            expand: true,
            cwd: "./vendor/",
            src: "./**",
            dest: "./demo/vendor/"
          }
        ]
      },
      build: {
        files: [
          {
            expand: true,
            cwd: "./src/images/",
            src: "./**",
            dest: "./build/images/"
          },
          {
            src:'./src/css/conversation.css',
            dest:'./build/css/RongIMWidget.css'
          }
        ]
      },
      release:{
        files:[
          {
            expand: true,
            cwd: "./src/images/",
            src: "./**",
            dest: "./dist/images/"
          },
          {
            src:'./src/css/conversation.css',
            dest:'./dist/css/RongIMWidget.css'
          }
        ]
      }
    },

    connect: {
      demo: {
        options: {
          port: 8000,
          hostname: '*',
          open: true,
          keepalive: true,
          base: ['./demo/']
        }
      }
    },

    typescript: {
      build: {
        src: ["./src/ts/**/*.module.ts","./src/ts/**/*.ts"],
        option: {
          module: 'amd', //or commonjs
          target: 'es5', //or es3
          sourceMap: true,
          declaration: false
        },
        dest: "./temp/main.js"
      }
    },

    watch: {
      demo: {
        options: {
          spawn: false
        },
        files: ["./src/**"],
        tasks: ["build", "clean:demo", "copy:demo"]
      }
    },

    concat: {
      build: {
        files:[
          {
            src:[
              './temp/main.js',
              './temp/myAppHTMLCache.js'
            ],
            dest:'./build/RongIMWidget.js'
          }
        ]
      },
      release:{
        files:[
          {
            src:[
              './temp/main.js',
              './temp/myAppHTMLCache.js'
            ],
            dest:'./dist/RongIMWidget.js'
          }
        ]
      }
    },
    uglify:{
      release:{
        files:[
          {
            src:'./dist/RongIMWidget.js',
            dest:'./dist/RongIMWidget.min.js'
          }
        ]
      }
    },
    cssmin:{
      release:{
        src:'./dist/css/RongIMWidget.css',
        dest:'./dist/css/RongIMWidget.min.css',
      }
    },
    ngtemplates: {
      app: {
        src: ["./src/ts/**/*.tpl.html"],
        dest: "./temp/myAppHTMLCache.js",
        options: {
          module: 'RongWebIMWidget', //name of our app
          htmlmin: {
            collapseBooleanAttributes: true,
            collapseWhitespace: true,
            removeAttributeQuotes: true,
            removeComments: true,
            removeEmptyAttributes: true,
            removeRedundantAttributes: true,
            removeScriptTypeAttributes: true,
            removeStyleLinkTypeAttributes: true
          }
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks("grunt-contrib-clean");
  grunt.loadNpmTasks('grunt-typescript');
  grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-angular-templates');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-cssmin');

  grunt.registerTask("default", function() {
    grunt.log.writeln("env" + process.env.path);
  });

  grunt.registerTask("build", ["clean:build", "typescript",
    "ngtemplates:app","concat:build", "copy:build","clean:temp"
  ]);

  grunt.registerTask("release", ["clean:release", "typescript",
    "ngtemplates:app","concat:release", "copy:release","clean:temp","uglify:release","cssmin:release"
  ]);


  grunt.registerTask("demo", ["build", "clean:demo", "copy:demo",
    "watch:demo"
  ]);

}
