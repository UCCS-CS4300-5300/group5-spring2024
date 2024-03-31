window.addEventListener('load', function(){
  // canvas setup
  const canvas = document.getElementById('canvas1');
  const ctx = canvas.getContext('2d');
  canvas.width = 500;
  canvas.height = 500;

  // game functions
  class InputHandler {  // class for handling input
    constructor(game){
      this.game = game;
      window.addEventListener('keydown', e => {  //If an arrow key is pressed
        if ((   (e.key === 'ArrowUp') ||
                (e.key === 'ArrowDown') ||
                (e.key === 'ArrowLeft') ||
                (e.key === 'ArrowRight')
             ) && this.game.keys.indexOf(e.key) === -1){  // for the first time
          this.game.keys.push(e.key);
        } else if (e.key === ' '){
          this.game.player.shootTop();
        }
        console.log(this.game.keys);
      });
      window.addEventListener('keyup', e => {
        if (this.game.keys.indexOf(e.key) > -1){  //If an arrow key is released
          this.game.keys.splice(this.game.keys.indexOf(e.key), 1);
        }
        console.log(this.game.keys);
      });
    }
  }
  class Projectile {  // class to create and handle projectiles
    constructor(game, x, y){
      this.game = game; 
      this.x = x;
      this.y = y;
      this.width = 5;
      this.height = 15;
      this.speed = 8;
      this.markedForDeletion = false;
    }
    update(){
      this.y -= this.speed;
      if (this.y < this.game.height * 0.1) this.markedForDeletion = true;
    }
    draw(context){
      context.fillStyle = 'red';
      context.fillRect((this.x + this.game.player.width * 0.5), this.y, this.width, this.height)
    }
  }
  class Particle {  // class to create and handle particles
    
  }
  class Player {  // class to create and handle player
    constructor(game){
      this.game = game;  //player variables 
      this.width = 100;
      this.height = 100;
      this.x = 200;  
      this.y = 400;
      this.speedY = 0;
      this.speedX = 0;
      this.maxSpeed = 3;
      this.projectiles = [];
    }
    update(){
      if (this.game.keys.includes('ArrowUp')) this.speedY = -this.maxSpeed;
      else if (this.game.keys.includes('ArrowDown')) this.speedY = this.maxSpeed;
      else this.speedY = 0;

      if (this.game.keys.includes('ArrowLeft')) this.speedX = -this.maxSpeed;
      else if (this.game.keys.includes('ArrowRight')) this.speedX = this.maxSpeed;
      else this.speedX = 0;
      
      this.y += this.speedY;
      this.x += this.speedX;

      //Handle Projectiles
      this.projectiles.forEach(projectile => {
        projectile.update();
      });
      this.projectiles = this.projectiles.filter(projectile => !projectile.markedForDeletion);
    }
    draw(context){
      context.fillStyle = 'grey';
      context.fillRect(this.x, this.y, this.width, this.height);
      this.projectiles.forEach(projectile => {
        projectile.draw(context);
      });
    }
    shootTop(){
      this.projectiles.push(new Projectile(this.game, this.x, this.y));
    }
    /*
    constructor(game) {
      this.game = game;
      this.width = 100;
      this.height = 100;
      this.x = canvas.width / 2;
      this.y = canvas.height / 2;
      this.speed = 5;
      this.angle = 0;
      this.frameX = 0;
      this.frameY = 0;
      this.frame = 0;
      this.spriteWidth = 498;
      this.spriteHeight = 327;
      this.lives = 3;
      this.cooldown = 0;
      this.frames = [
        { spriteX: 0, spriteY: 0 },
        { spriteX: 498, spriteY: 0 },
        { spriteX: 0, spriteY: 327 },
        { spriteX: 498, spriteY: 327 },
      ];
    }*/
  }
  class Enemy {}
  class Layer {}
  class Background {}
  class UI {}
  class Game {
    constructor(width, height){
      this.width = width;
      this.height = height;
      this.player = new Player(this);
      this.input = new InputHandler(this);
      this.keys = [];
    }
    update(){
      this.player.update();
    }
    draw(context){
      this.player.draw(context);
    }
  }

  const game = new Game(canvas.width, canvas.height);

  function animate(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    game.update();
    game.draw(ctx);
    requestAnimationFrame(animate);
  }
  animate();
});