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
      });
      window.addEventListener('keyup', e => {
        if (this.game.keys.indexOf(e.key) > -1){  //If an arrow key is released
          this.game.keys.splice(this.game.keys.indexOf(e.key), 1);
        }
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
      if(this.game.ammo > 0){
        this.projectiles.push(new Projectile(this.game, this.x, this.y));
        this.game.ammo--;
      }
    }
  }
  class Enemy {}
  class Layer {}
  class Background {}
  class UI {
    constructor(game){
      this.game = game;
      this.fontSize = 25;
      this.fontFamily = 'Helvetica';
      this.color = 'white';
      //this.textAlign = 'left';
      //this.textBaseline = 'top';
      //this.score = 0;
      //this.ammo = 10;
    }
    draw(context){
      //context.font = this.fontSize + 'px ' + this.fontFamily;
      context.fillStyle = this.color;
      for (let i = 0; i < this.game.ammo; i++){
        context.fillRect(20 + 5 * i, 50, 3, 20);
      }
      //context.textAlign = this.textAlign;
      //context.textBaseline = this.textBaseline;
      //context.fillText('Score: ' + this.score, 10, 10);
      //context.fillText('Ammo: ' + this.ammo, 10, 40);
    }
  }
  class Game {
    constructor(width, height){
      this.width = width;
      this.height = height;
      this.player = new Player(this);
      this.input = new InputHandler(this);
      this.ui = new UI(this);
      this.keys = [];
      this.ammo = 20;
      this.maxAmmo = 50;
      this.ammoTimer = 0;
      this.ammoInterval = 500;
    }
    update(deltaTime){
      this.player.update();
      if (this.ammoTimer > this.ammoInterval){
        if (this.ammo < this.maxAmmo){
          this.ammo++;
        }
        this.ammoTimer = 0;
      } else {
        this.ammoTime += deltaTime;
      }
    }
    draw(context){
      this.player.draw(context);
      this.ui.draw(context);
    }
  }

  const game = new Game(canvas.width, canvas.height);
  let lastTime = 0;
  function animate(timeStamp){
    const deltaTime = timeStamp - lastTime;
    lastTime = timeStamp;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    game.update(deltaTime);
    game.draw(ctx);
    requestAnimationFrame(animate);
  }
  animate(0);
});