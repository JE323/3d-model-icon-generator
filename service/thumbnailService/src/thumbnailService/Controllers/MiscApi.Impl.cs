using Microsoft.AspNetCore.Mvc;
using thumbnailService.Models;

namespace thumbnailService.Controllers;

/// <inheritdoc />
public class MiscApiControllerImpl : MiscApiController
{
    /// <inheritdoc />
    public override IActionResult GetPing() => new OkObjectResult(new InlineResponse200());
}
