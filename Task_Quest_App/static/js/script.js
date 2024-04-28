window.addEventListener('load', function(){
  // canvas setup
  const canvas = document.getElementById('canvas1');
  const ctx = canvas.getContext('2d');
  canvas.width = 540;
  canvas.height = 700;

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
    //Continuously updates the Projectile's position and properties
    update(){
      this.y -= this.speed;
      if (this.y < this.game.height * 0.1) this.markedForDeletion = true;
    }
    //Display the Projectile
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
      this.width = 52;
      this.height = 68;
      this.x = 250;  
      this.y = 600;
      this.speedY = 0;
      this.speedX = 0;
      this.maxSpeed = 3;
      this.projectiles = [];
      this.image = document.getElementById('Player');
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
      //context.fillStyle = 'grey';
      //context.fillRect(this.x, this.y, this.width, this.height);
      context.drawImage(this.image, this.x, this.y);
      this.projectiles.forEach(projectile => {
        projectile.draw(context);
      });
    }
    //Create a new Projectile
    shootTop(){
      if(this.game.ammo > 0){
        this.projectiles.push(new Projectile(this.game, this.x, this.y));
        this.game.ammo--;
      }
    }
  }
  
  class Enemy {    //Class to create and handle enemies
    constructor(game){
      this.game = game;        //Enemy variables
      this.y = 0;
      this.speedY = Math.random() * 1.5 + 0.5;
      this.markedForDeletion = false;
      this.lives = 5;
      this.score = this.lives;
      this.image = document.getElementById('Fighter');
    }

    update(){
      this.y += this.speedY;
      if (this.y + this.height < 0) this.markedForDeletion = true;
    }

    draw(context){
      //context.fillStyle = 'red';
      //context.fillRect(this.x, this.y, this.width, this.height);
      context.drawImage(this.image, this.x, this.y);
      //context.fillStyle = 'black';
      //context.font = '20px Arial';
      //context.fillText(this.lives, this.x, this.y);
    }
  }
  //Subclass of Enemy
  class Fighter extends Enemy {
    constructor(game){
      super(game);
      this.width = 87;
      this.height = 102;
      this.x = Math.random() * (this.game.width * 0.9 - this.width);
    }
  }

//Class to create and handle image layers  
  class Layer {
    constructor(game, image, speedModifier){
      this.game = game;
      this.image = image;
      this.speedModifier = speedModifier;
      this.width = 540;
      this.height = 960;
      this.x = 0;
      this.y = 0;
    }

    update(){
      if (this.y >= this.height) this.y = 0;
      this.y += this.game.speed * this.speedModifier;
    }

    draw(context){
      context.drawImage(this.image, this.x, this.y);
      context.drawImage(this.image, this.x, this.y - this.height);
    }
  }

  //Class to create and handle the background
  class Background {
    constructor(game){
      this.game = game;
      this.image1 = document.getElementById('layer1');
      this.layer1 = new Layer(this.game, this.image1, 1);
      this.layers = [this.layer1];
    }

    update(){
      this.layers.forEach(layer => layer.update());
    }

    draw(context){
      this.layers.forEach(layer => layer.draw(context));
    }
  }

  //Class to create and handle the User Interface
  class UI {
    constructor(game){
      this.game = game;
      this.fontSize = 25;
      this.fontFamily = 'Helvetica';
      this.color = 'lime';
    }
    draw(context){      
      //Ammo Counter
      context.fillStyle = this.color;
      for (let i = 0; i < this.game.ammo; i++){
        context.fillRect(20 + 5 * i, 10, 3, 20);
      }

      //Timer
      const formattedTime = (this.game.gameTime * 0.001).toFixed(1);
      context.fillText('Timer: ' + formattedTime, 20, 50);
      
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

        document.formName.inputName.value=5;

      }
    }
  }

  //Main Class to create and control all elements of a game
  class Game {
    constructor(width, height){      //Game variables
      this.width = width;
      this.height = height;
      this.background = new Background(this);
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
      this.winningScore = 30;
      this.gameTime = 0;
      this.timeLimit = 20000;
      this.speed = 1;
    }
    
    update(deltaTime){
      //Tracks time since game started
      if (!this.gameOver) this.gameTime += deltaTime;

      //Ends the game when time runs out
      if (this.gameTime > this.timeLimit) this.gameOver = true;

      this.background.update();
      this.player.update();

      //Regenerates ammo
      if (this.ammoTimer > this.ammoInterval){
        if (this.ammo < this.maxAmmo){
          this.ammo++;
        }
        this.ammoTimer = 0;
      } else {
        this.ammoTimer += deltaTime;
      }

      //Handles enemy collisions with player
      this.enemies.forEach(enemy => {
        enemy.update();
        if (this.checkCollision(this.player, enemy)){
          enemy.markedForDeletion = true;
        }

        //Handles enemy collisions with projectiles
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
      //Deletes enemies that are marked for deletion
      this.enemies = this.enemies.filter(enemy => !enemy.markedForDeletion);

      //Spawns enemies when the game is not over
      if (this.enemyTimer > this.enemyInterval && !this.gameOver){
        this.addEnemy();
        this.enemyTimer = 0;
      } else {
        this.enemyTimer += deltaTime;
      }
    }

    //Draws all the game elements
    draw(context){
      this.background.draw(context);
      
      this.player.draw(context);
      
      this.ui.draw(context);

      this.enemies.forEach(enemy => {
        enemy.draw(context);
      });
    }

    //Method to create a new enemy
    addEnemy(){
      this.enemies.push(new Fighter(this));
    }

    //Method to check for collision between two objects
    checkCollision(rect1, rect2){
      return (rect1.x < rect2.x + rect2.width &&
              rect1.x + rect1.width > rect2.x &&
              rect1.y < rect2.y + rect2.height &&
              rect1.height + rect1.y > rect2.y);
    }
  }

  //Creates a game object
  const game = new Game(canvas.width, canvas.height);

  //Variable to track time
  let lastTime = 0;

  //Method that Updates the game and draws it
  function animate(timeStamp){
    const deltaTime = timeStamp - lastTime;
    lastTime = timeStamp;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    game.update(deltaTime);
    game.draw(ctx);
    requestAnimationFrame(animate);
  }

  //Update and draw the game
  animate(0);
});