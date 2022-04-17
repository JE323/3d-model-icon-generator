using System;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using thumbnailService.Context;

namespace thumbnailService
{
    /// <summary>
    /// Program
    /// </summary>
    public class Program
    {
        const int SQL_CONN_ATTEMPTS = 10;
        const int SQL_CONN_DELAY_SEC = 2;
        
        /// <summary>
        /// Main
        /// </summary>
        /// <param name="args"></param>
        public static void Main(string[] args)
        {
            var host = CreateHostBuilder(args).Build();
            DbInit(host);
            host.Run();
        }

        private static void DbInit(IHost host)
        {
            using (var scope = host.Services.CreateScope())
            {
                var services = scope.ServiceProvider;

                ModelThumbnailDBContext context;

                bool connected = false;
                try
                {
                    context = services.GetRequiredService<ModelThumbnailDBContext>();
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Exception raised: {ex}");
                    Console.WriteLine($"Unable to get SQL context!");
                    throw;
                }

                for (int i = 0; i < SQL_CONN_ATTEMPTS; i++)
                {
                    try
                    {
                        if (context.Database.CanConnect())
                        {
                            try
                            {
                                context.Database.EnsureCreated();
                                connected = true;
                                break;
                            }
                            catch
                            {
                                Console.WriteLine($"Database attempt failed on: {i}");
                            }
                        }
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine(e);
                        throw;
                    }
                    
                    System.Threading.Thread.Sleep( new TimeSpan(0, 0, SQL_CONN_DELAY_SEC));
                }

                Console.WriteLine(connected ? "Successfully connected to PSQL database." : "Unable to establish connection to PSQL database");

            }
        }

        /// <summary>
        /// Create the host builder.
        /// </summary>
        /// <param name="args"></param>
        /// <returns>IHostBuilder</returns>
        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                   webBuilder.UseStartup<Startup>();
                             // .UseUrls("http://0.0.0.0:8080/");
                    Console.WriteLine("Started successfully!");
                });
    }
}
