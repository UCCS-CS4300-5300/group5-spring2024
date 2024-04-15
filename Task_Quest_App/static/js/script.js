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
      this.x = x + this.game.player.width * 0.5;
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
      context.fillStyle = 'lime';
      context.fillRect((this.x), this.y, this.width, this.height)
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
  class Enemy {
    constructor(game){
      this.game = game;
      this.y = 0;
      this.speedY = Math.random() * 1.5 + 0.5;
      this.markedForDeletion = false;
      this.lives = 5;
      this.score = this.lives;
    }
    update(){
      this.y += this.speedY;
      if (this.y + this.height < 0) this.markedForDeletion = true;
    }
    draw(context){
      context.fillStyle = 'red';
      context.fillRect(this.x, this.y, this.width, this.height);
      context.fillStyle = 'black';
      context.font = '20px Arial';
      context.fillText(this.lives, this.x, this.y);
    }
  }
  class Fighter extends Enemy {
    constructor(game){
      super(game);
      this.width = 20;
      this.height = 20;
      this.x = Math.random() * (this.game.width * 0.9 - this.width);
    }
  }

  
  class Layer {}
  class Background {}
  class UI {
    constructor(game){
      this.game = game;
      this.fontSize = 25;
      this.fontFamily = 'Helvetica';
      this.color = 'lime';
      //this.textAlign = 'left';
      //this.textBaseline = 'top';
      //this.score = 0;
      //this.ammo = 10;
    }
    draw(context){
      //context.font = this.fontSize + 'px ' + this.fontFamily;
      
      //Ammo Counter
      context.fillStyle = this.color;
      for (let i = 0; i < this.game.ammo; i++){
        context.fillRect(20 + 5 * i, 50, 3, 20);
      }
      //context.textAlign = this.textAlign;
      //context.textBaseline = this.textBaseline;
      //context.fillText('Score: ' + this.score, 10, 10);
      //context.fillText('Ammo: ' + this.ammo, 10, 40);

      //Timer
      const formattedTime = (this.game.gameTime * 0.001).toFixed(1);
      context.fillText('Timer: ' + formattedTime, 20, 100);
      
      //Game Over Message
      if (this.game.gameOver){
        context.textAlign = 'center';
        let message1;
        let message2;
        if (this.game.score > this.game.winningScore){
          message1 = "You Win!";
          message2 = "Well Done!";
        } else {
          message1 = "You Lose!";
          message2 = "Try Again!";
        }
        context.font = '50px ' + this.fontFamily;
        context.fillText(message1, this.game.width * 0.5, this.game.height * 0.5 - 40);
        context.font = '25px ' + this.fontFamily;
        context.fillText(message2, this.game.width * 0.5, this.game.height * 0.5 + 40);
      }
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
      this.enemies = [];
      this.enemyTimer = 0;
      this.enemyInterval = 1000;
      this.ammo = 20;
      this.maxAmmo = 50;
      this.ammoTimer = 0;
      this.ammoInterval = 500;
      this.score = 0;
      this.gameOver = false;
      this.score = 0;
      this.winningScore = 1;
      this.gameTime = 0;
      this.timeLimit = 5000;
    }
    
    update(deltaTime){
      //Tracks time since game started
      if (!this.gameOver) this.gameTime += deltaTime;

      if (this.gameTime > this.timeLimit) this.gameOver = true;
      this.player.update();
      
      if (this.ammoTimer > this.ammoInterval){
        if (this.ammo < this.maxAmmo){
          this.ammo++;
        }
        this.ammoTimer = 0;
      } else {
        this.ammoTimer += deltaTime;
      }
      
      this.enemies.forEach(enemy => {
        enemy.update();
        if (this.checkCollision(this.player, enemy)){
          enemy.markedForDeletion = true;
        }
        
        this.player.projectiles.forEach(projectile => {
          if (this.checkCollision(projectile, enemy)) {
            enemy.lives--;
            projectile.markedForDeletion = true;
            if (enemy.lives <= 0){
              enemy.markedForDeletion = true;
              if (!this.gameOver) this.score += enemy.score;
              if (this.score > this.winningScore) this.gameOver = true;
            }
          }
        });
      });
      
      this.enemies = this.enemies.filter(enemy => !enemy.markedForDeletion);
      
      if (this.enemyTimer > this.enemyInterval && !this.gameOver){
        this.addEnemy();
        this.enemyTimer = 0;
      } else {
        this.enemyTimer += deltaTime;
      }
    }
    
    draw(context){
      this.player.draw(context);
      
      this.ui.draw(context);

      this.enemies.forEach(enemy => {
        enemy.draw(context);
      });
    }

    addEnemy(){
      this.enemies.push(new Fighter(this));
    }

    checkCollision(rect1, rect2){
      return (rect1.x < rect2.x + rect2.width &&
              rect1.x + rect1.width > rect2.x &&
              rect1.y < rect2.y + rect2.height &&
              rect1.height + rect1.y > rect2.y);
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